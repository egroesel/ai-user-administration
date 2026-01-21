# Backend Dokumentation

FastAPI-basiertes Backend für die Nutzerverwaltung.

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
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Aktueller Benutzer
- `POST /api/auth/password-reset-request` - Passwort-Reset anfordern
- `POST /api/auth/password-reset-confirm` - Passwort zurücksetzen

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

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
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