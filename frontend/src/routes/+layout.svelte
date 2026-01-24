<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { language, t } from '$lib/stores/language';

	onMount(() => {
		auth.checkAuth();
	});
</script>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
	<nav class="bg-white dark:bg-gray-800 shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between h-16">
				<div class="flex items-center space-x-8">
					<a href="/" class="text-xl font-bold text-[#304b50] dark:text-white">
						#startneu
					</a>

					<!-- Main Navigation -->
					<div class="hidden sm:flex items-center space-x-6">
						<a
							href="/projects/new"
							class="text-gray-700 dark:text-gray-300 hover:text-[#06E481] dark:hover:text-[#06E481] transition-colors font-medium"
						>
							{$t('nav.startProject')}
						</a>
						<a
							href="/discover"
							class="text-gray-700 dark:text-gray-300 hover:text-[#06E481] dark:hover:text-[#06E481] transition-colors font-medium"
						>
							{$t('nav.discover')}
						</a>
						<a
							href="/community"
							class="text-gray-700 dark:text-gray-300 hover:text-[#06E481] dark:hover:text-[#06E481] transition-colors font-medium"
						>
							{$t('nav.community')}
						</a>
					</div>
				</div>

				<div class="flex items-center space-x-4">
					<!-- Language Toggle -->
					<button
						on:click={() => language.toggle()}
						class="p-2 text-gray-600 dark:text-gray-300 hover:text-[#263c40] dark:hover:text-[#33f79f] transition-colors"
						title={$language === 'de' ? 'Switch to English' : 'Auf Deutsch wechseln'}
					>
						<span class="text-sm font-medium">{$language === 'de' ? 'EN' : 'DE'}</span>
					</button>

					<!-- Theme Toggle -->
					<button
						on:click={() => theme.toggle()}
						class="p-2 text-gray-600 dark:text-gray-300 hover:text-[#263c40] dark:hover:text-[#33f79f] transition-colors"
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
							class="text-gray-700 dark:text-gray-300 hover:text-[#263c40] dark:hover:text-[#33f79f]"
							>{$t('nav.profile')}</a
						>
					{:else}
						<a
							href="/login"
							class="text-gray-700 dark:text-gray-300 hover:text-[#263c40] dark:hover:text-[#33f79f]"
							>{$t('nav.login')}</a
						>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<main>
		<slot />
	</main>

	<!-- Admin Button (fixed bottom right) -->
	{#if $auth.isAdmin}
		<a
			href="/admin"
			class="fixed bottom-6 right-6 p-3 bg-gray-800 dark:bg-gray-700 text-white rounded-full shadow-lg hover:bg-gray-700 dark:hover:bg-gray-600 transition-colors z-50"
			title={$t('nav.admin')}
		>
			<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
			</svg>
		</a>
	{/if}
</div>
