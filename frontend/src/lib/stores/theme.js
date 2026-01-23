import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function createThemeStore() {
	const defaultTheme = browser
		? localStorage.getItem('theme') ||
			(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
		: 'light';

	const { subscribe, set, update } = writable(defaultTheme);

	function applyTheme(theme) {
		if (browser) {
			if (theme === 'dark') {
				document.documentElement.classList.add('dark');
			} else {
				document.documentElement.classList.remove('dark');
			}
			localStorage.setItem('theme', theme);
		}
	}

	// Apply initial theme
	if (browser) {
		applyTheme(defaultTheme);
	}

	return {
		subscribe,
		toggle: () => {
			update((current) => {
				const newTheme = current === 'dark' ? 'light' : 'dark';
				applyTheme(newTheme);
				return newTheme;
			});
		},
		set: (theme) => {
			applyTheme(theme);
			set(theme);
		}
	};
}

export const theme = createThemeStore();
