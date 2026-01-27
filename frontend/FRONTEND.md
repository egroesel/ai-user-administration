# Frontend Dokumentation

SvelteKit-basiertes Frontend für den Startnext Crowdfunding-Plattform Prototypen.

## Technologie-Stack

- **Framework**: SvelteKit 2.0
- **Styling**: Tailwind CSS 3.4
- **Build Tool**: Vite 5.0
- **Runtime**: Node.js 18+
- **CMS**: Storyblok (Headless CMS)

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

## Storyblok CMS

Storyblok wird als Headless CMS für Content-Seiten (Impressum, Datenschutz, etc.) verwendet.

### Konfiguration

Die Storyblok-Konfiguration befindet sich in `src/lib/storyblok.js`:

```javascript
import { storyblokInit, apiPlugin } from '@storyblok/svelte';

storyblokInit({
  accessToken: 'your-access-token',
  use: [apiPlugin],
  apiOptions: { region: 'eu' },
  components: {
    page: Page,
    teaser: Teaser,
    feature: Feature,
    grid: Grid,
    richtext: RichText
  }
});
```

### Verfügbare Komponenten

| Komponente | Beschreibung | Felder |
|------------|--------------|--------|
| `page` | Seitencontainer | `body` (Bloks) |
| `teaser` | Hero/Teaser-Bereich | `headline`, `subheadline`, `image` |
| `feature` | Feature-Karte | `name`, `description`, `icon`, `link` |
| `grid` | Grid-Layout | `headline`, `columns`, `columns_content` |
| `richtext` | Rich-Text-Inhalt | `content` (Richtext) |

### Routing

Content-Seiten werden über eine Catch-All-Route ausgeliefert:

- `/impressum` → Story mit Slug `impressum`
- `/datenschutz` → Story mit Slug `datenschutz`
- `/ueber-uns/team` → Story mit Slug `ueber-uns/team`

Die Route befindet sich in `src/routes/[...slug]/`.

### Visual Editor

Für den Storyblok Visual Editor ist HTTPS erforderlich. In der Entwicklung wird dies durch `vite-plugin-mkcert` ermöglicht:

```javascript
// vite.config.js
import mkcert from 'vite-plugin-mkcert';

export default defineConfig({
  plugins: [sveltekit(), mkcert()],
  server: {
    https: true
  }
});
```

Preview-URL im Storyblok: `https://localhost:5173/`

### Neue Komponente erstellen

1. Svelte-Komponente in `src/lib/components/storyblok/` erstellen
2. Komponente in `src/lib/storyblok.js` registrieren
3. Block-Typ mit gleichen Namen in Storyblok anlegen
