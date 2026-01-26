# Frontend Dokumentation

SvelteKit-basiertes Frontend für den Startnext Crowdfunding-Plattform Prototypen.

## Technologie-Stack

- **Framework**: SvelteKit 2.0
- **Styling**: Tailwind CSS 3.4
- **Build Tool**: Vite 5.0
- **Runtime**: Node.js 18+

## Installation

### 1. Node.js Dependencies installieren

```bash
cd frontend
npm install
```

### 2. Umgebungsvariablen konfigurieren

```bash
cp .env.example .env
```

Bearbeite `.env`:

```env
PUBLIC_API_URL=http://localhost:8000
```

## Frontend starten

### Development Mode

```bash
npm run dev
```

Das Frontend läuft nun auf: `http://localhost:5173`

Änderungen werden automatisch im Browser aktualisiert (Hot Module Replacement).

### Production Build

```bash
npm run build
```

Build-Verzeichnis: `build/`

### Production Preview

```bash
npm run preview
```

## Projektstruktur

```
frontend/
├── src/
│   ├── lib/
│   │   └── api.js              # API Client
│   ├── routes/                 # Seiten (File-based Routing)
│   │   ├── +layout.svelte      # Layout (Navigation)
│   │   ├── +page.svelte        # Startseite
│   │   ├── login/
│   │   │   └── +page.svelte    # Login-Seite
│   │   ├── register/
│   │   │   └── +page.svelte    # Registrierungs-Seite
│   │   ├── profile/
│   │   │   └── +page.svelte    # Profil-Seite
│   │   ├── admin/
│   │   │   ├── +page.svelte    # Admin-Dashboard
│   │   │   └── email-test/
│   │   │       └── +page.svelte # Email-Test-Seite
│   │   ├── forgot-password/
│   │   │   └── +page.svelte    # Passwort vergessen
│   │   └── reset-password/
│   │       └── +page.svelte    # Passwort zurücksetzen
│   ├── app.html                # HTML Template
│   └── app.css                 # Tailwind CSS
├── package.json
├── svelte.config.js
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Verfügbare Skripte

```bash
# Development Server starten
npm run dev

# Production Build erstellen
npm run build

# Production Preview
npm run preview
```

## Routing (File-based)

SvelteKit nutzt File-based Routing:

- `/` → `src/routes/+page.svelte`
- `/login` → `src/routes/login/+page.svelte`
- `/profile` → `src/routes/profile/+page.svelte`
- `/admin` → `src/routes/admin/+page.svelte`

## Deployment

### Vercel

```bash
npm i -g vercel
vercel
```

### Netlify

```bash
npm i -g netlify-cli
netlify deploy --prod
```

### Static Hosting (Nginx, Apache)

```bash
# In svelte.config.js
import adapter from '@sveltejs/adapter-static';

export default {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build'
		})
	}
};
```

Dann:

```bash
npm run build
```

Die Dateien in `build/` können auf jeden Static-Host kopiert werden.
