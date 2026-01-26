from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import get_db
import models
import schemas
from security import get_current_user, get_current_user_optional
import re
from typing import Optional, List

router = APIRouter(prefix="/api/projects", tags=["Projects"])


def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from a title."""
    slug = title.lower()
    # Replace German umlauts
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue'
    }
    for char, replacement in replacements.items():
        slug = slug.replace(char, replacement)
    # Replace spaces and special chars with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def ensure_unique_slug(db: Session, slug: str, exclude_id: Optional[int] = None) -> str:
    """Ensure the slug is unique, adding a number suffix if necessary."""
    base_slug = slug
    counter = 1
    while True:
        query = db.query(models.Project).filter(models.Project.slug == slug)
        if exclude_id:
            query = query.filter(models.Project.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@router.get("/suggest-slug", response_model=schemas.SlugSuggestion)
def suggest_slug(
    title: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Generate a unique slug suggestion from a title."""
    base_slug = generate_slug(title)
    unique_slug = ensure_unique_slug(db, base_slug)
    return {"slug": unique_slug}


@router.post("", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project."""
    # Ensure slug is unique
    unique_slug = ensure_unique_slug(db, project.slug)
    if unique_slug != project.slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slug '{project.slug}' is already taken. Try '{unique_slug}' instead."
        )

    db_project = models.Project(
        owner_id=current_user.id,
        title=project.title,
        slug=project.slug,
        description=project.description,
        short_description=project.short_description,
        funding_goal=project.funding_goal,
        image_url=project.image_url,
        video_url=project.video_url,
        project_type=project.project_type,
        plan=project.plan,
        provision=project.provision,
        voucher_code=project.voucher_code,
        start_date=project.start_date,
        status="draft"
    )
    db.add(db_project)

    # Mark user as starter if not already
    if not current_user.is_starter:
        current_user.is_starter = True

    db.commit()
    db.refresh(db_project)

    return db_project


@router.get("", response_model=List[schemas.ProjectListResponse])
def list_projects(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all public projects (verified, financing, ended_success, ended_failed)."""
    query = db.query(models.Project).options(
        joinedload(models.Project.owner)
    ).filter(
        models.Project.status.in_(["verified", "financing", "ended_success", "ended_failed"])
    )

    if status:
        query = query.filter(models.Project.status == status)

    projects = query.order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects


@router.get("/featured", response_model=List[schemas.ProjectListResponse])
def list_featured_projects(
    limit: int = Query(4, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get featured projects (financing projects, ordered by funding progress)."""
    projects = db.query(models.Project).options(
        joinedload(models.Project.owner)
    ).filter(
        models.Project.status == "financing"
    ).order_by(
        models.Project.funding_current.desc()
    ).limit(limit).all()
    return projects


@router.get("/near-goal", response_model=List[schemas.ProjectListResponse])
def list_near_goal_projects(
    min_percentage: int = Query(80, ge=0, le=100),
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get projects that are near their funding goal (default 80%+)."""
    # Get financing projects where funding_current >= min_percentage% of funding_goal
    projects = db.query(models.Project).options(
        joinedload(models.Project.owner)
    ).filter(
        models.Project.status == "financing",
        models.Project.funding_goal > 0,
        models.Project.funding_current >= models.Project.funding_goal * (min_percentage / 100)
    ).order_by(
        (models.Project.funding_current / models.Project.funding_goal).desc()
    ).limit(limit).all()
    return projects


@router.get("/my-projects", response_model=List[schemas.ProjectListResponse])
def list_my_projects(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all projects owned by the current user."""
    projects = db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).order_by(models.Project.created_at.desc()).all()
    return projects


@router.get("/{slug}", response_model=schemas.ProjectResponse)
def get_project(
    slug: str,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get a project by slug."""
    project = db.query(models.Project).filter(models.Project.slug == slug).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Draft projects are only visible to owner and admins
    if project.status == "draft":
        if not current_user or (current_user.id != project.owner_id and not current_user.is_admin):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

    # Submitted projects are only visible to owner and admins
    if project.status == "submitted":
        if not current_user or (current_user.id != project.owner_id and not current_user.is_admin):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

    return project


@router.put("/{slug}", response_model=schemas.ProjectResponse)
def update_project(
    slug: str,
    project_update: schemas.ProjectUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project (owner or admin can update, only draft/submitted status for non-admins)."""
    project = db.query(models.Project).filter(models.Project.slug == slug).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check authorization: owner or admin
    is_owner = project.owner_id == current_user.id
    is_admin = current_user.is_admin

    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project"
        )

    # Non-admins can only update draft/submitted projects
    if not is_admin and project.status not in ["draft", "submitted"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update project after verification"
        )

    update_data = project_update.model_dump(exclude_unset=True)

    # If slug is being updated, slugify it first and ensure it's unique
    if "slug" in update_data and update_data["slug"]:
        # Slugify the input
        slugified = generate_slug(update_data["slug"])
        if slugified != project.slug:
            unique_slug = ensure_unique_slug(db, slugified, project.id)
            if unique_slug != slugified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Slug '{slugified}' is already taken. Try '{unique_slug}' instead."
                )
            update_data["slug"] = slugified
        else:
            # No change needed
            del update_data["slug"]

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    slug: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project (only owner can delete, only draft status)."""
    project = db.query(models.Project).filter(models.Project.slug == slug).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project"
        )

    if project.status != "draft" and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete draft projects"
        )

    db.delete(project)
    db.commit()


@router.post("/{slug}/submit", response_model=schemas.ProjectResponse)
def submit_project(
    slug: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a project for review."""
    project = db.query(models.Project).filter(models.Project.slug == slug).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to submit this project"
        )

    if project.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft projects can be submitted"
        )

    # Basic validation before submission
    if not project.title or not project.description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project must have a title and description before submission"
        )

    project.status = "submitted"
    project.submitted_at = func.now()

    db.commit()
    db.refresh(project)

    return project


@router.post("/{slug}/duplicate", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def duplicate_project(
    slug: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Duplicate a project. Creates a new draft copy owned by the current user."""
    project = db.query(models.Project).filter(models.Project.slug == slug).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Only owner or admin can duplicate
    if project.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to duplicate this project"
        )

    # Generate unique slug for the duplicate
    base_slug = f"{project.slug}-copy"
    unique_slug = ensure_unique_slug(db, base_slug)

    # Create duplicate project (start_date not copied - new project gets new date)
    duplicate = models.Project(
        owner_id=current_user.id,
        title=f"{project.title} (Copy)",
        slug=unique_slug,
        description=project.description,
        short_description=project.short_description,
        funding_goal=project.funding_goal,
        image_url=project.image_url,
        video_url=project.video_url,
        project_type=project.project_type,
        plan=project.plan,
        provision=project.provision,
        voucher_code=project.voucher_code,
        status="draft"
    )
    db.add(duplicate)
    db.commit()
    db.refresh(duplicate)

    return duplicate
