<script>
	import '../app.css';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { language, t } from '$lib/stores/language';
	import { logout } from '$lib/api';

	onMount(() => {
		auth.checkAuth();
	});

	async function handleLogout() {
		try {
			await logout();
			goto('/login');
		} catch (error) {
			console.error('Logout failed:', error);
			auth.clear();
			goto('/login');
		}
	}
</script>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
	<nav class="bg-white dark:bg-gray-800 shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between h-16">
				<div class="flex items-center">
					<a href="/" class="text-xl font-bold text-gray-800 dark:text-white"
						>{$t('nav.title')}</a
					>
				</div>

				<div class="flex items-center space-x-4">
					<!-- Language Toggle -->
					<button
						on:click={() => language.toggle()}
						class="p-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
						title={$language === 'de' ? 'Switch to English' : 'Auf Deutsch wechseln'}
					>
						<span class="text-sm font-medium">{$language === 'de' ? 'EN' : 'DE'}</span>
					</button>

					<!-- Theme Toggle -->
					<button
						on:click={() => theme.toggle()}
						class="p-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
						title={$t('theme.toggle')}
					>
						{#if $theme === 'dark'}
							<!-- Sun Icon -->
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-5 w-5"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
								/>
							</svg>
						{:else}
							<!-- Moon Icon -->
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-5 w-5"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
								/>
							</svg>
						{/if}
					</button>

					<div class="h-6 w-px bg-gray-300 dark:bg-gray-600"></div>

					{#if $auth.isAuthenticated}
						<a
							href="/profile"
							class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
							>{$t('nav.profile')}</a
						>
						{#if $auth.isAdmin}
							<a
								href="/admin"
								class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
								>{$t('nav.admin')}</a
							>
						{/if}
						<button
							on:click={handleLogout}
							class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
						>
							{$t('nav.logout')}
						</button>
					{:else}
						<a
							href="/login"
							class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
							>{$t('nav.login')}</a
						>
						<a
							href="/register"
							class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
							>{$t('nav.register')}</a
						>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<main>
		<slot />
	</main>
</div>
