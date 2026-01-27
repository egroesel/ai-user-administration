# Backend Dokumentation

FastAPI-basiertes Backend für den Startnext Crowdfunding-Plattform Prototypen.

## Technologie-Stack

- **Framework**: FastAPI 0.109.0
- **Datenbank**: PostgreSQL (via SQLAlchemy)
- **Authentifizierung**: JWT (python-jose) + bcrypt
- **Email**: Resend
- **2FA**: PyOTP (TOTP)

## Installation

### 1. Python Virtual Environment

```bash
cd backend
python -m venv venv

# Aktivieren
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. PostgreSQL Datenbank erstellen

```bash
# PostgreSQL starten
brew services start postgresql  # macOS
sudo systemctl start postgresql # Linux

# Datenbank erstellen
createdb user_management
```

### 4. Umgebungsvariablen konfigurieren

```bash
cp .env.example .env
```

Bearbeite `.env` und setze folgende Werte:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/user_management

# Security (generiere einen sicheren Schlüssel)
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (Resend)
RESEND_API_KEY=re_your_resend_api_key
FROM_EMAIL=noreply@yourdomain.com

# Application
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000

# Admin user (wird beim ersten Start erstellt)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=changeme123
```

#### SECRET_KEY generieren

Der `SECRET_KEY` wird verwendet, um JWT-Tokens zu signieren und ist kritisch für die Sicherheit.

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Wichtig:**
- Der SECRET_KEY muss mindestens 32 Zeichen lang sein
- Verwende NIEMALS den Beispiel-Key in Produktion
- Bei Änderung des SECRET_KEY müssen sich alle Benutzer neu anmelden

**Was passiert bei .env-Änderungen:**
- `.env`-Datei wird nur beim **Start** eingelesen
- Bei Änderungen: Backend **neu starten** (Code-Änderungen mit `--reload` werden automatisch geladen)
- SECRET_KEY-Änderung invalidiert alle existierenden JWT-Tokens

## Backend starten

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Das Backend läuft nun auf: `http://localhost:8000`
API-Dokumentation: `http://localhost:8000/docs`

## Projektstruktur

```
backend/
├── routers/                # API Endpoints
│   ├── auth.py            # Authentifizierung
│   ├── users.py           # Benutzerprofil
│   ├── admin.py           # Admin-Funktionen
│   └── two_factor.py      # 2FA
├── config.py              # Konfiguration
├── database.py            # Datenbankverbindung
├── models.py              # SQLAlchemy Models
├── schemas.py             # Pydantic Schemas
├── security.py            # Authentifizierungslogik
├── email_service.py       # E-Mail-Funktionen
├── two_factor.py          # 2FA-Logik
├── main.py                # Hauptanwendung
└── requirements.txt       # Python Dependencies
```

## API-Endpunkte

### Authentifizierung

- `POST /api/auth/register` - Registrierung
- `POST /api/auth/login` - Login (mit Passwort)
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Aktueller Benutzer
- `POST /api/auth/password-reset-request` - Passwort-Reset anfordern
- `POST /api/auth/password-reset-confirm` - Passwort zurücksetzen
- `POST /api/auth/magic-link/request` - Magic Link anfordern (passwordless)
- `POST /api/auth/magic-link/verify` - Magic Link verifizieren

### Benutzer

- `GET /api/users/profile` - Profil abrufen
- `PUT /api/users/profile` - Profil aktualisieren

### Admin

- `GET /api/admin/users` - Alle Benutzer auflisten
- `GET /api/admin/users/{user_id}` - Benutzer abrufen
- `PATCH /api/admin/users/{user_id}` - Benutzer aktualisieren
- `DELETE /api/admin/users/{user_id}` - Benutzer löschen
- `POST /api/admin/test-email` - Test-Emails versenden

### Two-Factor Authentication

- `POST /api/2fa/setup` - 2FA einrichten
- `POST /api/2fa/verify` - 2FA verifizieren
- `POST /api/2fa/disable` - 2FA deaktivieren

### AI Coach

Der KI-gestützte Projektassistent hilft Nutzern bei der Entwicklung ihrer Projektideen.

- `POST /api/ai-coach/generate` - Nachricht an den AI Coach senden
- `GET /api/ai-coach/threads/{thread_id}` - Thread-Verlauf abrufen
- `POST /api/ai-coach/threads/{thread_id}/claim` - Thread bei Login übernehmen
- `GET /api/ai-coach/settings` - AI Coach Einstellungen abrufen
- `POST /api/ai-coach/drafts/generate/{thread_id}` - Projektentwurf generieren
- `GET /api/ai-coach/drafts/{thread_id}` - Projektentwurf abrufen
- `PATCH /api/ai-coach/drafts/{thread_id}` - Projektentwurf aktualisieren
- `POST /api/ai-coach/drafts/{thread_id}/convert` - Entwurf in Projekt umwandeln

#### Konfiguration

In der `.env`:

```env
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ASSISTANT_ID=asst_your_assistant_id

# AI Coach Settings (optional)
AI_MAX_ANONYMOUS_MESSAGES=5    # Max Nachrichten ohne Login
AI_MIN_MESSAGES_FOR_PROJECT=3  # Min Nachrichten für Projekterstellung
AI_MAX_ANONYMOUS_DRAFTS=2      # Max Entwürfe ohne Login
```

#### Funktionsweise

1. **Anonyme Nutzung**: Nutzer können ohne Login bis zu 5 Nachrichten senden und 2 Projektentwürfe erstellen
2. **Session-Tracking**: Anonyme Nutzer werden über eine Session-ID identifiziert
3. **Thread-Übernahme**: Bei Login werden anonyme Threads dem Nutzer zugeordnet
4. **Projekterstellung**: Nach genügend Konversation kann ein Projektentwurf generiert werden

## Datenbank-Modelle

### User

```python
- id: Integer (Primary Key)
- email: String (Unique)
- hashed_password: String
- full_name: String (Optional)
- is_active: Boolean
- is_admin: Boolean
- created_at: DateTime
- updated_at: DateTime
- two_factor_enabled: Boolean
- two_factor_secret: String (Optional)
- reset_token: String (Optional)
- reset_token_expires: DateTime (Optional)
- magic_link_token: String (Optional)
- magic_link_expires: DateTime (Optional)
```

### Session

```python
- id: Integer (Primary Key)
- user_id: Integer
- session_token: String (Unique)
- created_at: DateTime
- expires_at: DateTime
- ip_address: String (Optional)
- user_agent: String (Optional)
```

## Sicherheit

### Passwort-Hashing

Passwörter werden mit bcrypt gehasht:

```python
import bcrypt

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

### JWT-Tokens

Tokens werden mit HS256 und dem SECRET_KEY signiert:

```python
from jose import jwt

encoded_jwt = jwt.encode(
    {"sub": str(user_id), "exp": expire_time},
    SECRET_KEY,
    algorithm="HS256"
)
```

### 2FA (TOTP)

Two-Factor-Authentication basiert auf TOTP (Time-based One-Time Password):

```python
import pyotp

# Secret generieren
secret = pyotp.random_base32()

# Code verifizieren
totp = pyotp.TOTP(secret)
is_valid = totp.verify(user_code, valid_window=1)
```

## Email-Versand

### Konfiguration

Emails werden über Resend versendet. Konfiguriere in der `.env`:

```env
RESEND_API_KEY=re_your_api_key
FROM_EMAIL=noreply@yourdomain.com
```

### Email-Typen

- **Welcome Email**: Bei Registrierung
- **Password Reset**: Mit Reset-Link
- **Magic Link**: Passwordless Login-Link
- **Account Activated**: Admin-Benachrichtigung
- **Account Deactivated**: Admin-Benachrichtigung
- **Test Emails**: Für Admin-Tests

### Test-Emails senden

```python
from email_service import send_test_email

send_test_email(
    email="test@example.com",
    email_type="welcome",  # oder password_reset, account_activated, etc.
    user_name="Test User"
)
```

## Entwicklung

### Backend Tests ausführen

```bash
pytest
```

### Datenbank-Migrationen (Alembic)

Alembic verwaltet Datenbankschema-Änderungen. Die Konfiguration befindet sich in:
- `alembic.ini` - Hauptkonfiguration
- `alembic/env.py` - Umgebungskonfiguration (lädt DATABASE_URL aus settings)
- `alembic/versions/` - Migrationsdateien

#### Befehle

```bash
# Migration ausführen (alle ausstehenden)
alembic upgrade head

# Neue Migration erstellen (nach Model-Änderung)
alembic revision --autogenerate -m "beschreibung der änderung"

# Migrationen anzeigen
alembic history

# Aktuelle Version anzeigen
alembic current

# Eine Migration zurückrollen
alembic downgrade -1

# Zu spezifischer Version migrieren
alembic upgrade <revision_id>
```

#### Neue Migration erstellen

1. **Model ändern** in `models.py`:
```python
class User(Base):
    # Neue Spalte hinzufügen
    new_field = Column(String(255), nullable=True)
```

2. **Migration generieren**:
```bash
alembic revision --autogenerate -m "add new_field to users"
```

3. **Migration prüfen** in `alembic/versions/`:
```python
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('users', 'new_field')
```

4. **Migration ausführen**:
```bash
alembic upgrade head
```

#### Wichtige Regeln für Live-Datenbanken

- **Neue Spalten**: Immer `nullable=True` oder mit Default-Wert
- **Spalten löschen**: In separater Migration, nachdem Code angepasst wurde
- **Spalten umbenennen**: Neue Spalte erstellen → Daten kopieren → Alte löschen (3 Migrationen)
- **Backups**: Vor jeder Migration in Produktion
- **Testen**: Migrationen zuerst lokal oder auf Staging testen

#### Railway Deployment

Der `Procfile` führt Migrationen automatisch vor dem App-Start aus:

```
web: alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

#### Manuelle Migration (ohne autogenerate)

```bash
alembic revision -m "custom migration"
```

Dann die `upgrade()` und `downgrade()` Funktionen manuell schreiben:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('magic_link_token', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('magic_link_expires', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    op.drop_column('users', 'magic_link_expires')
    op.drop_column('users', 'magic_link_token')
```

### Code-Qualität

```bash
# Linting
flake8 .

# Type Checking
mypy .

# Formatting
black .
```

## Troubleshooting

### Datenbank-Verbindungsfehler

```bash
# Prüfe PostgreSQL Status
pg_isready
brew services list  # macOS

# Prüfe DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Import-Fehler oder bcrypt-Fehler

```bash
# Aktiviere Virtual Environment
source venv/bin/activate

# Entferne alte Versionen
pip uninstall -y bcrypt passlib

# Installiere Dependencies neu
pip install -r requirements.txt
```

### Email wird nicht versendet

1. Prüfe `RESEND_API_KEY` in der `.env`
2. Verifiziere deine Domain bei Resend
3. Prüfe die FROM_EMAIL - sie muss von einer verifizierten Domain sein

### 2FA funktioniert nicht

1. Stelle sicher, dass die Systemzeit korrekt ist (TOTP ist zeitbasiert)
2. `valid_window=1` ist bereits implementiert für eine Toleranz von ±30 Sekunden

## Produktions-Deployment

### 1. ASGI Server

Verwende Gunicorn mit Uvicorn Workers:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### 2. Umgebungsvariablen

- Nutze **keine** `.env`-Dateien in Produktion
- Verwende Secret Manager (AWS Secrets Manager, Azure Key Vault, etc.)
- Setze Environment Variables über dein Hosting-System

### 3. Sicherheit

- Generiere einen **sicheren** SECRET_KEY (min. 32 Zeichen)
- Nutze **HTTPS** (z.B. über Nginx/Traefik)
- Setze sichere **CORS**-Einstellungen
- Implementiere **Rate Limiting**
- Aktiviere **Logging** und **Monitoring**

### 4. Datenbank

- Nutze eine **managed** PostgreSQL-Instanz (AWS RDS, DigitalOcean, etc.)
- Implementiere **Backups**
- Verwende **Connection Pooling**