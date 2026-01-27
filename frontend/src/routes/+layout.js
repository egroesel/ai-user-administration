// SSR Configuration for SvelteKit
// ================================
//
// For Capacitor (iOS/Android):
//   - SSR must be disabled because mobile apps can't run a server
//   - Build with: BUILD_TARGET=capacitor npm run build
//   - All routing happens client-side
//
// For Vercel (web):
//   - SSR is enabled for better SEO and faster initial page load
//   - Build with: npm run build (default)
//   - Server renders pages on each request
//
// The VITE_BUILD_TARGET env var is replaced at build time by Vite

export const ssr = import.meta.env.VITE_BUILD_TARGET !== 'capacitor';
