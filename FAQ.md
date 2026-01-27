# Häufig gestellte Fragen (FAQ)

## Installation & Setup

### Muss ich das Backend neu bauen, wenn sich eine .env-Variable ändert?

**Nein**, aber du musst das Backend **neu starten**:

```bash
# Stoppe den Server (Strg+C)
# Dann starte neu:
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Die `.env`-Datei wird nur beim **Start** eingelesen, nicht kontinuierlich.

**Hinweis**: Das `--reload` Flag lädt Code-Änderungen automatisch, aber **nicht** `.env`-Änderungen.

### Welche Python-Version wird benötigt?

Python 3.9 oder höher wird empfohlen.

```bash
python --version  # Sollte 3.9+ sein
```

### Welche Node.js-Version wird benötigt?

Node.js 18 oder höher wird empfohlen.

```bash
node --version  # Sollte 18+ sein
```

### Wie richte ich PostgreSQL ein?

```bash
# macOS
brew install postgresql
brew services start postgresql
createdb user_management

# Linux (Ubuntu/Debian)
sudo apt install postgresql
sudo systemctl start postgresql
sudo -u postgres createdb user_management

# Docker (Alternative)
docker run --name postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=user_management -p 5432:5432 -d postgres:14
```

## Sicherheit

### Wofür ist der SECRET_KEY?

Der `SECRET_KEY` ist essentiell für die Sicherheit:

- **Signiert JWT-Tokens**: Verhindert Fälschung von Authentifizierungs-Tokens
- **Validiert Anfragen**: Nur mit dem richtigen Key sind Tokens gültig
- **Wie ein Master-Passwort**: Schützt die gesamte API

**Wichtig**: Bei Änderung des SECRET_KEY müssen sich alle Benutzer neu anmelden.

### Wie generiere ich einen sicheren SECRET_KEY?

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Das erzeugt einen kryptografisch sicheren, 32-Zeichen-Key.

**Beispiel-Output**: `kJ8vN9mL3pQ2xR5tY7wZ1aB4cD6eF9gH0iJ2kL5mN8oP`

Trage diesen in die `backend/.env` ein:

```env
SECRET_KEY=kJ8vN9mL3pQ2xR5tY7wZ1aB4cD6eF9gH0iJ2kL5mN8oP
```

### Ist der Default SECRET_KEY sicher?

**Nein!** Der Beispiel-Key `your-secret-key-change-this-in-production` ist **NICHT** für Produktion geeignet.

Du **musst** einen eigenen Key generieren vor dem produktiven Einsatz.

### Was passiert, wenn ich den SECRET_KEY ändere?

- Alle JWT-Tokens werden **ungültig**
- Alle Benutzer müssen sich **neu anmelden**
- Sessions werden **zurückgesetzt**

### Wie sichere ich meine .env-Datei?

1. **Niemals** in Git committen (ist in `.gitignore`)
2. In Produktion: Nutze einen **Secret Manager** (AWS Secrets Manager, Azure Key Vault, etc.)
3. Setze **restriktive Dateirechte**: `chmod 600 .env`
4. Verwende **verschiedene Keys** für Development/Staging/Production

## Emails

### Welche Emails werden automatisch versendet?

- **Registrierung**: Willkommens-Email an neue Benutzer
- **Passwort-Reset**: Email mit Reset-Link (1 Stunde gültig)
- **Admin-Test**: Verschiedene Test-Emails (nur manuell von Admins)

### Wie teste ich den Email-Versand?

1. Melde dich als Admin an
2. Gehe zu **Admin → Email-Test**
3. Wähle einen Email-Typ:
   - **Einfache Test-Email**: Grundlegende Test-Email
   - **Willkommens-Email**: Für neue Benutzer
   - **Passwort zurücksetzen**: Mit Test-Token
   - **Account aktiviert**: Benachrichtigung
   - **Account deaktiviert**: Benachrichtigung
4. Gib deine Email-Adresse ein
5. Klicke "Test-Email senden"

### Warum werden Emails nicht versendet?

**Prüfe folgendes:**

1. **Resend API Key**: Ist er korrekt in `.env` gesetzt?
   ```bash
   cat backend/.env | grep RESEND_API_KEY
   ```

2. **Domain verifiziert**: Hast du deine Domain bei Resend verifiziert?
   - Login auf [resend.com](https://resend.com)
   - Gehe zu "Domains"
   - Füge DNS-Records hinzu

3. **FROM_EMAIL**: Muss von einer verifizierten Domain sein
   ```env
   FROM_EMAIL=noreply@deine-domain.com
   ```

4. **Backend neu gestartet**: Nach .env-Änderungen Backend neu starten

### Kann ich einen anderen Email-Provider nutzen?

Ja, aber du musst `email_service.py` anpassen. Resend ist vorkonfiguriert, aber du kannst auch SMTP, SendGrid, Mailgun, etc. nutzen.

## Authentifizierung & Benutzer

### Was passiert, wenn ich das Admin-Passwort ändere?

Nach Änderung des `ADMIN_PASSWORD` in der `backend/.env`:

1. Backend neu starten
2. Das Passwort wird **nicht** automatisch aktualisiert für existierende Admins
3. Der Admin-User wird nur beim **ersten Start** erstellt
4. Ändere das Passwort stattdessen über das **Profil** im Frontend

### Wie füge ich weitere Admins hinzu?

1. Erstelle einen normalen Benutzer über **Registrierung**
2. Melde dich als **Admin** an
3. Gehe zum **Admin-Panel**
4. Klicke bei dem Benutzer auf **"Admin machen"**

### Wie ändere ich mein Passwort?

1. Melde dich an
2. Gehe zu **Profil**
3. Gib ein neues Passwort ein
4. Klicke **"Profil aktualisieren"**

### Was ist die Passwort-Policy?

- Mindestens **8 Zeichen** lang
- Wird mit **bcrypt** gehasht
- Keine weiteren Einschränkungen (kann erweitert werden)

### Wie funktioniert Passwort-Reset?

1. Klicke auf "Passwort vergessen?" beim Login
2. Gib deine Email-Adresse ein
3. Du erhältst eine Email mit einem Reset-Link
4. Der Link ist **1 Stunde** gültig
5. Setze ein neues Passwort

## Datei-Uploads (Avatare & Projektbilder)

### Wie lade ich ein Profilbild hoch?

1. Gehe zu **Profil → Einstellungen**
2. Klicke auf **"Avatar hochladen"**
3. Wähle ein Bild aus (max. 5 MB, JPG/PNG)
4. Das Bild wird sofort gespeichert

### Wie lade ich ein Projektbild hoch?

1. Öffne dein Projekt
2. Aktiviere den **Bearbeitungsmodus**
3. Klicke auf das Projektbild
4. Wähle **"Bild hochladen"** oder gib eine externe URL ein

### Welche Dateiformate werden unterstützt?

- **Bilder**: JPG, JPEG, PNG, GIF, WebP
- **Maximale Größe**: 5 MB pro Datei

### Wo werden die Dateien gespeichert?

**Lokal (Development)**:
```
backend/uploads/
├── avatars/      # Profilbilder
└── projects/     # Projektbilder
```

**Produktion (Railway)**:
- Nutze ein **Persistent Volume** für dauerhafte Speicherung
- Konfiguriere `UPLOAD_DIR` als Environment Variable

### Wie richte ich Railway Volumes ein?

1. Gehe zu deinem Railway-Projekt
2. Klicke auf **"New Volume"**
3. Setze den **Mount Path**: `/app/uploads`
4. Füge die Environment Variable hinzu:
   ```env
   UPLOAD_DIR=/app/uploads
   ```

### Warum werden Bilder nicht angezeigt?

**Prüfe folgendes:**

1. **Backend läuft**: Bilder werden über `/uploads/...` ausgeliefert
2. **VITE_API_URL korrekt**: Frontend muss die vollständige URL kennen
   ```env
   VITE_API_URL=http://localhost:8000
   ```
3. **Datei existiert**: Prüfe ob die Datei im `uploads/`-Ordner liegt
4. **Berechtigungen**: Der Ordner muss beschreibbar sein
   ```bash
   chmod -R 755 backend/uploads
   ```

### Kann ich externe Bild-URLs verwenden?

Ja, bei Projektbildern kannst du auch eine **externe URL** eingeben (z.B. von Unsplash, Cloudinary, etc.). Das Bild wird dann nicht lokal gespeichert.

### Wie lösche ich ein hochgeladenes Bild?

**Avatar**:
1. Gehe zu **Profil → Einstellungen**
2. Klicke auf **"Avatar löschen"**

**Projektbild**:
1. Aktiviere den **Bearbeitungsmodus** im Projekt
2. Klicke auf das Bild
3. Klicke auf **"Bild löschen"**

### Werden alte Bilder automatisch gelöscht?

Ja, wenn du ein neues Bild hochlädst, wird das alte automatisch vom Server entfernt.

## Two-Factor Authentication (2FA)

### Wie aktiviere ich 2FA?

1. Gehe zu deinem **Profil**
2. Klicke auf **"2FA einrichten"**
3. Scanne den QR-Code mit einer Authenticator-App:
   - Google Authenticator
   - Authy
   - Microsoft Authenticator
   - 1Password
4. Gib den 6-stelligen Code ein
5. Klicke **"2FA aktivieren"**

### 2FA-Code wird nicht akzeptiert

**Mögliche Ursachen:**

1. **Systemzeit falsch**: TOTP ist zeitbasiert
   ```bash
   # macOS
   sudo ntpdate -u time.apple.com

   # Linux
   sudo ntpdate -u pool.ntp.org
   ```

2. **Falscher Code**: Warte auf den nächsten Code (alle 30 Sekunden)

3. **Toleranz-Fenster**: Bereits implementiert (`valid_window=1` = ±30 Sekunden)

### Wie deaktiviere ich 2FA?

1. Gehe zu deinem **Profil**
2. Gib den aktuellen 6-stelligen Code ein
3. Klicke **"2FA deaktivieren"**

### Ich habe mein 2FA-Gerät verloren

Als Admin:
1. Melde dich im **Admin-Panel** an (mit einem Admin-Account)
2. Setze den Benutzer zurück (oder kontaktiere einen anderen Admin)

Für dich selbst ohne Admin-Zugang:
- Derzeit keine Self-Service-Option
- Kontaktiere einen Administrator
- **Empfehlung**: Backup-Codes implementieren (zukünftiges Feature)

## Admin-Panel

### Wer kann auf das Admin-Panel zugreifen?

Nur Benutzer mit `is_admin=True`.

Der erste Admin wird automatisch beim Backend-Start erstellt (aus `.env`).

### Kann ich einen Admin wieder zum normalen User machen?

Ja, im Admin-Panel:
1. Klicke bei einem Admin-Benutzer auf **"Admin entziehen"**

**Achtung**: Du kannst dir selbst **nicht** die Admin-Rechte entziehen.

### Kann ich mich selbst als Admin löschen?

**Nein**, das System verhindert das aus Sicherheitsgründen.

## Entwicklung

### Wie starte ich Frontend und Backend gleichzeitig?

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Oder mit Concurrently (optional):**

```bash
# Im Root-Verzeichnis
npm install -g concurrently

# Dann:
concurrently "cd backend && source venv/bin/activate && uvicorn main:app --reload" "cd frontend && npm run dev"
```

### Wie resette ich die Datenbank?

```bash
# PostgreSQL
dropdb user_management
createdb user_management

# Dann Backend neu starten (erstellt Tabellen neu)
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Achtung**: Alle Daten gehen verloren!

### Gibt es ein Test-System?

Derzeit nicht implementiert, aber empfohlen:

**Backend**:
```bash
cd backend
pip install pytest pytest-cov
pytest
```

**Frontend**:
```bash
cd frontend
npm install -D @playwright/test
npx playwright test
```

## Deployment

### Kann ich das in Produktion einsetzen?

Ja, aber beachte:

1. **SECRET_KEY**: Sicheren Key generieren
2. **HTTPS**: Nutze SSL/TLS (Let's Encrypt, Cloudflare, etc.)
3. **PostgreSQL**: Managed Database (AWS RDS, DigitalOcean, etc.)
4. **Environment Variables**: Secret Manager nutzen (kein `.env`)
5. **Rate Limiting**: Implementieren (gegen Brute-Force)
6. **Monitoring**: Logging und Error-Tracking (Sentry, etc.)
7. **Backups**: Automatische Datenbank-Backups

### Welche Hosting-Optionen gibt es?

**Backend**:
- **DigitalOcean App Platform**
- **Railway**
- **Fly.io**
- **AWS Elastic Beanstalk**
- **Google Cloud Run**
- **Heroku** (mit Gunicorn)

**Frontend**:
- **Vercel** (empfohlen für SvelteKit)
- **Netlify**
- **Cloudflare Pages**
- **AWS S3 + CloudFront**

**Datenbank**:
- **DigitalOcean Managed Databases**
- **AWS RDS**
- **Supabase** (PostgreSQL)
- **Railway** (PostgreSQL)

### Wie deploye ich auf Vercel?

**Frontend**:
```bash
cd frontend
vercel
```

**Backend**: Vercel unterstützt kein Python direkt, nutze Railway oder DigitalOcean.

## Fehlerbehebung

### "Failed to fetch" Fehler im Frontend

1. **Backend läuft nicht**: Starte das Backend
   ```bash
   curl http://localhost:8000/health
   ```

2. **CORS-Fehler**: Prüfe `FRONTEND_URL` in `backend/.env`
   ```env
   FRONTEND_URL=http://localhost:5173
   ```

3. **Falscher API_URL**: Prüfe `frontend/.env`
   ```env
   VITE_API_URL=http://localhost:8000
   ```

### "Database connection error"

1. **PostgreSQL läuft nicht**:
   ```bash
   brew services start postgresql  # macOS
   sudo systemctl start postgresql # Linux
   ```

2. **Falsche DATABASE_URL**:
   ```bash
   cat backend/.env | grep DATABASE_URL
   ```

3. **Datenbank existiert nicht**:
   ```bash
   createdb user_management
   ```

### "Import Error" im Backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Build-Fehler

```bash
cd frontend
rm -rf node_modules .svelte-kit package-lock.json
npm install
npm run build
```

## Performance

### Wie viele Benutzer kann das System verwalten?

Das System ist für kleine bis mittlere Deployments ausgelegt:

- **< 1000 Benutzer**: Problemlos
- **1000 - 10.000 Benutzer**: Mit Optimierungen (Caching, Connection Pooling)
- **> 10.000 Benutzer**: Weitere Optimierungen nötig (Load Balancing, Replicas, etc.)

### Kann ich das System skalieren?

Ja, empfohlene Maßnahmen:

1. **Load Balancer**: Nginx/Traefik vor mehreren Backend-Instanzen
2. **Database Replicas**: Read-Replicas für PostgreSQL
3. **Caching**: Redis für Sessions/Tokens
4. **CDN**: Für Frontend (Cloudflare, etc.)
5. **Connection Pooling**: PgBouncer für PostgreSQL

## Weitere Hilfe

- **Backend**: Siehe [backend/BACKEND.md](backend/BACKEND.md)
- **Frontend**: Siehe [frontend/FRONTEND.md](frontend/FRONTEND.md)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
