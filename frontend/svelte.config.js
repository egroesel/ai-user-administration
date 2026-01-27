// adapter-auto: Automatically detects deployment platform (Vercel, Netlify, etc.)
// Enables SSR and serverless functions for better SEO and performance
import adapterAuto from '@sveltejs/adapter-auto';

// adapter-static: Generates pure static HTML/JS files
// Required for Capacitor because mobile apps can't run a Node.js server
import adapterStatic from '@sveltejs/adapter-static';

import preprocess from 'svelte-preprocess';

// VITE_BUILD_TARGET=capacitor switches to static adapter for iOS/Android builds
// Default (no env var) uses auto adapter for Vercel deployment with SSR
// Note: We use process.env here because svelte.config.js runs in Node.js context
const isCapacitor = process.env.VITE_BUILD_TARGET === 'capacitor';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: preprocess(),
	kit: {
		adapter: isCapacitor
			? adapterStatic({
				pages: 'build',
				assets: 'build',
				fallback: 'index.html',  // SPA fallback - all routes serve index.html
				precompress: false,
				strict: false
			})
			: adapterAuto()  // Vercel auto-detects and configures SSR
	}
};

export default config;
