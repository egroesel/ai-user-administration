from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import schemas
from security import get_current_user, get_current_user_optional
from config import settings
from typing import Optional, List
import uuid
import openai
from openai import OpenAIError, AuthenticationError, APIError
import markdown
import re
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/ai-coach", tags=["AI Coach"])

# Initialize OpenAI client
client = None
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY not in ["", "your-key", "your-openai-api-key"]:
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# System prompt for the AI Coach
SYSTEM_PROMPT = """Du bist ein freundlicher und erfahrener Crowdfunding-Coach bei startnext.
Deine Aufgabe ist es, Nutzer:innen dabei zu helfen, ihre Projektideen zu entwickeln und zu verfeinern.

Verhalte dich wie ein erfahrener Berater:
- Stelle gezielte Fragen, um die Projektidee besser zu verstehen
- Hilf dabei, das Fundingziel realistisch einzuschätzen
- Frage nach dem Projekttyp (Crowdfunding mit Dankeschöns, Fundraising/Spenden, oder privates Projekt)
- Frage nach dem gewünschten Tarif (Basic 9%, Pro 7%, Premium 5%, Enterprise individuell)
- Frage nach dem geplanten Startzeitpunkt und der Laufzeit (30-90 Tage)
- Gib hilfreiche Tipps für eine erfolgreiche Kampagne
- Sei ermutigend aber realistisch

Wichtige Regeln:
- Antworte immer auf Deutsch
- Halte deine Antworten prägnant (max. 150 Wörter)
- Stelle pro Nachricht maximal 2 Fragen
- Sei freundlich und motivierend
- Verwende keine Emojis"""

# Project generation prompts
PROJECT_PROMPTS = {
    "title": """Basierend auf unserem Gespräch: Wie ist der Projekttitel?
Gib nur den Titel aus, maximal 80 Zeichen, ohne Formatierung oder Emojis.""",

    "slug": """Erstelle einen URL-Kurznamen für das Projekt.
Nur Kleinbuchstaben, Zahlen und Bindestriche. Maximal 30 Zeichen.
Ersetze ä->ae, ö->oe, ü->ue, ß->ss. Gib nur den Kurznamen aus.""",

    "short_description": """Formuliere eine Kurzbeschreibung (max. 500 Zeichen).
Aus der ich/wir-Perspektive, ohne Emojis.
Beginne mit dem Grund, warum man das Projekt unterstützen sollte.""",

    "description": """Erstelle eine ausführliche Projektbeschreibung (max. 5000 Zeichen).
Erkläre: Worum geht es? Was wird unterstützt? Wer profitiert? Welcher Nutzen?
Gutes Storytelling, keine Marketing-Sprache, keine falschen Versprechen.""",

    "funding_goal": """Was ist das passende Fundingziel?
Antworte nur mit einer Zahl in Euro, ohne Währungszeichen.""",

    "project_type": """Welcher Projekttyp passt? Antworte nur mit einem Wort:
crowdfunding, fundraising oder private""",

    "plan": """Welcher Tarif wurde besprochen? Antworte nur mit einem Wort:
basic, pro, premium oder enterprise
Falls nicht besprochen: basic""",

    "start_date": """Wann soll das Projekt starten?
Antworte nur im Format YYYY-MM-DD.
Falls nicht besprochen: {current_date} + 14 Tage.""",

    "duration_days": """Wie lange soll die Kampagne laufen?
Antworte nur mit einer Zahl (30, 45, 60 oder 90).
Falls nicht besprochen: 45"""
}


def get_openai_client():
    """Get OpenAI client or raise error if not configured."""
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Coach is not configured. Please set OPENAI_API_KEY."
        )
    return client


def count_user_messages(thread: models.AIThread) -> int:
    """Count non-system user messages in a thread."""
    return sum(1 for msg in thread.messages if not msg.is_assistant and not msg.is_system)


def check_message_limits(thread: models.AIThread, user: Optional[models.User]) -> tuple[bool, bool]:
    """Check message limits and return (can_continue, requires_login)."""
    user_msg_count = count_user_messages(thread)

    if user:
        return True, False

    if user_msg_count >= settings.AI_MAX_ANONYMOUS_MESSAGES:
        return False, True

    return True, False


def can_create_project(thread: models.AIThread) -> bool:
    """Check if thread has enough messages to create a project."""
    user_msg_count = count_user_messages(thread)
    return user_msg_count >= settings.AI_MIN_MESSAGES_FOR_PROJECT


def build_conversation_history(thread: models.AIThread, include_system: bool = False) -> list[dict]:
    """Build OpenAI-compatible message history from thread."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Sort messages by creation time
    sorted_msgs = sorted(thread.messages, key=lambda m: m.created_at)

    for msg in sorted_msgs:
        if msg.is_system and not include_system:
            continue
        role = "assistant" if msg.is_assistant else "user"
        messages.append({"role": role, "content": msg.content})

    return messages


async def get_ai_response(openai_client, messages: list[dict], max_tokens: int = 500) -> tuple[str, int]:
    """Get response from OpenAI Chat API."""
    try:
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL if hasattr(settings, 'OPENAI_MODEL') else "gpt-4o-mini",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else None
        return content, tokens

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Coach authentication failed. Please check OPENAI_API_KEY."
        )
    except OpenAIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI Coach error: {str(e)}"
        )


@router.get("/settings", response_model=schemas.AISettingsResponse)
def get_ai_settings():
    """Get AI Coach settings (thresholds)."""
    return {
        "max_anonymous_messages": settings.AI_MAX_ANONYMOUS_MESSAGES,
        "min_messages_for_project": settings.AI_MIN_MESSAGES_FOR_PROJECT,
        "max_anonymous_drafts": settings.AI_MAX_ANONYMOUS_DRAFTS
    }


@router.post("/generate", response_model=schemas.AIGenerateResponse)
async def generate_message(
    request: schemas.AIGenerateRequest,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    openai_client = get_openai_client()

    thread = None

    # Find or create thread
    if request.thread_id:
        thread = db.query(models.AIThread).filter(
            models.AIThread.id == request.thread_id
        ).first()
        if not thread:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thread not found"
            )
    elif request.session_id and not current_user:
        thread = db.query(models.AIThread).filter(
            models.AIThread.session_id == request.session_id,
            models.AIThread.user_id.is_(None)
        ).first()

    # Create new thread if needed
    if not thread:
        thread = models.AIThread(
            id=str(uuid.uuid4()),
            openai_thread_id="",  # Not used with Chat API
            user_id=current_user.id if current_user else None,
            session_id=request.session_id if not current_user else None
        )
        db.add(thread)
        db.commit()
        db.refresh(thread)

    # Check message limits
    can_continue, requires_login = check_message_limits(thread, current_user)

    if not can_continue:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Message limit reached. Please log in to continue."
        )

    # Save user message to DB
    user_message = models.AIMessage(
        id=str(uuid.uuid4()),
        thread_id=thread.id,
        content=request.prompt,
        is_assistant=False,
        is_system=False
    )
    db.add(user_message)
    db.commit()
    db.refresh(thread)

    # Build conversation history and get AI response
    messages = build_conversation_history(thread)
    raw_reply, token_count = await get_ai_response(openai_client, messages)

    # Convert markdown to HTML
    html_reply = markdown.markdown(raw_reply)

    # Save assistant message to DB
    assistant_message = models.AIMessage(
        id=str(uuid.uuid4()),
        thread_id=thread.id,
        content=raw_reply,
        is_assistant=True,
        is_system=False,
        token_count=token_count
    )
    db.add(assistant_message)
    db.commit()

    # Reload thread
    db.refresh(thread)

    # Check limits for response
    _, next_requires_login = check_message_limits(thread, current_user)
    user_msg_count = count_user_messages(thread)

    return {
        "reply": html_reply,
        "raw_reply": raw_reply,
        "thread_id": thread.id,
        "message_count": user_msg_count,
        "can_create_project": can_create_project(thread),
        "requires_login": next_requires_login
    }


@router.get("/threads/{thread_id}", response_model=schemas.AIThreadResponse)
def get_thread(
    thread_id: str,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get a thread with all messages."""
    thread = db.query(models.AIThread).filter(
        models.AIThread.id == thread_id
    ).first()

    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )

    visible_messages = [msg for msg in thread.messages if not msg.is_system]

    return {
        "id": thread.id,
        "message_count": len(visible_messages),
        "user_message_count": count_user_messages(thread),
        "created_at": thread.created_at,
        "messages": sorted(visible_messages, key=lambda m: m.created_at)
    }


@router.get("/threads", response_model=List[schemas.AIThreadListItem])
def list_threads(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all threads for the current user."""
    threads = db.query(models.AIThread).filter(
        models.AIThread.user_id == current_user.id
    ).order_by(models.AIThread.created_at.desc()).all()

    result = []
    for thread in threads:
        first_user_msg = next(
            (msg for msg in thread.messages if not msg.is_assistant and not msg.is_system),
            None
        )
        result.append({
            "id": thread.id,
            "first_message": first_user_msg.content[:100] if first_user_msg else None,
            "message_count": len([m for m in thread.messages if not m.is_system]),
            "created_at": thread.created_at
        })

    return result


@router.post("/threads/{thread_id}/claim")
def claim_thread(
    thread_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Claim an anonymous thread after login. Also claims any associated draft."""
    thread = db.query(models.AIThread).filter(
        models.AIThread.id == thread_id,
        models.AIThread.user_id.is_(None)
    ).first()

    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found or already claimed"
        )

    thread.user_id = current_user.id
    thread.session_id = None

    # Also claim any associated draft
    draft = db.query(models.AIDraft).filter(
        models.AIDraft.thread_id == thread_id,
        models.AIDraft.user_id.is_(None)
    ).first()

    if draft:
        draft.user_id = current_user.id
        draft.session_id = None

    db.commit()

    return {"message": "Thread claimed successfully", "thread_id": thread.id}


@router.get("/drafts/{thread_id}", response_model=schemas.AIDraftResponse)
def get_draft(
    thread_id: str,
    session_id: Optional[str] = None,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get the draft for a thread. Anonymous users can access with session_id."""
    draft = db.query(models.AIDraft).filter(
        models.AIDraft.thread_id == thread_id
    ).first()

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Draft not found"
        )

    thread = db.query(models.AIThread).filter(
        models.AIThread.id == thread_id
    ).first()

    # Authorization check
    if current_user:
        # Logged in user: must own the thread/draft or be admin
        if thread.user_id != current_user.id and draft.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this draft"
            )
    else:
        # Anonymous user: must have matching session_id
        if not session_id or (draft.session_id != session_id and thread.session_id != session_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this draft"
            )

    return draft


@router.post("/drafts/generate/{thread_id}", response_model=schemas.AIDraftResponse)
async def generate_draft(
    thread_id: str,
    request: schemas.AIGenerateDraftRequest = None,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Generate a project draft from thread conversation. Anonymous users can generate up to 2 drafts."""
    openai_client = get_openai_client()

    thread = db.query(models.AIThread).filter(
        models.AIThread.id == thread_id
    ).first()

    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )

    # Get session_id from request or thread
    session_id = None
    if request and request.session_id:
        session_id = request.session_id
    elif thread.session_id:
        session_id = thread.session_id

    # Authorization check
    if current_user:
        # Logged in user: must own the thread or be admin
        if thread.user_id and thread.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
    else:
        # Anonymous user: must have session_id matching the thread
        if not session_id or thread.session_id != session_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

        # Check anonymous draft limit
        anonymous_draft_count = db.query(models.AIDraft).filter(
            models.AIDraft.session_id == session_id,
            models.AIDraft.user_id.is_(None)
        ).count()

        # Check if this thread already has a draft (regeneration is allowed)
        existing_thread_draft = db.query(models.AIDraft).filter(
            models.AIDraft.thread_id == thread_id
        ).first()

        if not existing_thread_draft and anonymous_draft_count >= settings.AI_MAX_ANONYMOUS_DRAFTS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Anonymous users can only generate {settings.AI_MAX_ANONYMOUS_DRAFTS} drafts. Please log in to continue."
            )

    if not can_create_project(thread):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Need at least {settings.AI_MIN_MESSAGES_FOR_PROJECT} messages to create a project"
        )

    existing_draft = db.query(models.AIDraft).filter(
        models.AIDraft.thread_id == thread_id
    ).first()

    if existing_draft and existing_draft.status == "converted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This thread has already been converted to a project"
        )

    # Build base conversation for context
    base_messages = build_conversation_history(thread)

    # Generate each field
    generated_data = {}

    extraction_system = """Du bist ein Daten-Extraktor. Basierend auf dem Gespräch,
extrahiere die angeforderten Informationen. Antworte NUR mit dem gefragten Wert, ohne Erklärung."""

    for field, prompt_template in PROJECT_PROMPTS.items():
        prompt = prompt_template.replace("{current_date}", datetime.now().strftime("%Y-%m-%d"))

        # Create extraction messages
        extraction_messages = [
            {"role": "system", "content": extraction_system},
            {"role": "user", "content": f"Hier ist das Gespräch:\n\n" +
                "\n".join([f"{m['role']}: {m['content']}" for m in base_messages[1:]]) +
                f"\n\nAufgabe: {prompt}"}
        ]

        try:
            response = openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL if hasattr(settings, 'OPENAI_MODEL') else "gpt-4o-mini",
                messages=extraction_messages,
                max_tokens=1000 if field == "description" else 200,
                temperature=0.3
            )
            generated_data[field] = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating {field}: {e}")
            continue

    # Parse generated data
    funding_goal = None
    if "funding_goal" in generated_data:
        try:
            funding_goal = float(re.sub(r'[^\d.]', '', generated_data["funding_goal"]))
        except:
            funding_goal = None

    duration_days = None
    if "duration_days" in generated_data:
        try:
            duration_days = int(re.sub(r'[^\d]', '', generated_data["duration_days"]))
        except:
            duration_days = 45

    start_date = None
    if "start_date" in generated_data:
        try:
            # Try to extract date from response
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', generated_data["start_date"])
            if date_match:
                start_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            else:
                start_date = datetime.now() + timedelta(days=14)
        except:
            start_date = datetime.now() + timedelta(days=14)

    # Sanitize slug
    slug = generated_data.get("slug", "").lower()
    slug = re.sub(r'[^a-z0-9-]', '', slug)[:30] or f"project-{uuid.uuid4().hex[:8]}"

    # Sanitize project_type
    project_type = generated_data.get("project_type", "crowdfunding").lower().strip()
    if project_type not in ["crowdfunding", "fundraising", "private"]:
        project_type = "crowdfunding"

    # Sanitize plan
    plan = generated_data.get("plan", "basic").lower().strip()
    if plan not in ["basic", "pro", "premium", "enterprise"]:
        plan = "basic"

    # Create or update draft
    if existing_draft:
        existing_draft.title = generated_data.get("title", "")[:255]
        existing_draft.slug = slug
        existing_draft.short_description = generated_data.get("short_description", "")[:500]
        existing_draft.description = generated_data.get("description", "")
        existing_draft.funding_goal = funding_goal
        existing_draft.project_type = project_type
        existing_draft.plan = plan
        existing_draft.start_date = start_date
        existing_draft.duration_days = duration_days
        if current_user:
            existing_draft.user_id = current_user.id
            existing_draft.session_id = None
        draft = existing_draft
    else:
        draft = models.AIDraft(
            thread_id=thread_id,
            user_id=current_user.id if current_user else None,
            session_id=session_id if not current_user else None,
            title=generated_data.get("title", "")[:255],
            slug=slug,
            short_description=generated_data.get("short_description", "")[:500],
            description=generated_data.get("description", ""),
            funding_goal=funding_goal,
            project_type=project_type,
            plan=plan,
            start_date=start_date,
            duration_days=duration_days,
            status="draft"
        )
        db.add(draft)

    db.commit()
    db.refresh(draft)

    return draft


@router.patch("/drafts/{thread_id}", response_model=schemas.AIDraftResponse)
def update_draft(
    thread_id: str,
    updates: schemas.AIDraftUpdate,
    session_id: Optional[str] = None,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Update a draft. Anonymous users can update with session_id."""
    draft = db.query(models.AIDraft).filter(
        models.AIDraft.thread_id == thread_id
    ).first()

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Draft not found"
        )

    # Authorization check
    if current_user:
        # Logged in user: must own the draft or be admin
        if draft.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
    else:
        # Anonymous user: must have matching session_id
        if not session_id or draft.session_id != session_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

    if draft.status == "converted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update converted draft"
        )

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(draft, field, value)

    db.commit()
    db.refresh(draft)

    return draft


@router.post("/drafts/{thread_id}/convert", response_model=schemas.ProjectResponse)
def convert_draft_to_project(
    thread_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Convert a draft to a real project."""
    draft = db.query(models.AIDraft).filter(
        models.AIDraft.thread_id == thread_id
    ).first()

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Draft not found"
        )

    if draft.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    if draft.status == "converted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Draft already converted"
        )

    if not draft.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Draft must have a title"
        )

    # Ensure unique slug
    slug = draft.slug or re.sub(r'[^a-z0-9-]', '-', draft.title.lower())[:50]
    base_slug = slug
    counter = 1
    while db.query(models.Project).filter(models.Project.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Calculate financing_end
    financing_end = None
    if draft.start_date and draft.duration_days:
        financing_end = draft.start_date + timedelta(days=draft.duration_days)

    # Determine provision based on plan
    plan_provisions = {
        "basic": 9.00,
        "pro": 7.00,
        "premium": 5.00,
        "enterprise": None
    }
    plan = draft.plan or "basic"
    provision = plan_provisions.get(plan, 9.00)

    # Create project
    project = models.Project(
        owner_id=current_user.id,
        title=draft.title,
        slug=slug,
        description=draft.description,
        short_description=draft.short_description,
        funding_goal=draft.funding_goal,
        project_type=draft.project_type or "crowdfunding",
        plan=plan,
        provision=provision,
        start_date=draft.start_date,
        financing_end=financing_end,
        status="draft",
        ai_generated=True,
        ai_thread_id=thread_id
    )
    db.add(project)

    # Mark user as starter
    if not current_user.is_starter:
        current_user.is_starter = True

    # Update draft status
    draft.status = "converted"
    draft.converted_project_id = project.id

    db.commit()
    db.refresh(project)

    return project
