<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { verifyMagicLink } from '$lib/api';
	import { t } from '$lib/stores/language';

	let status = 'verifying'; // 'verifying', 'success', 'error'
	let error = '';

	onMount(async () => {
		const token = $page.url.searchParams.get('token');

		if (!token) {
			status = 'error';
			error = $t('magicLink.noToken');
			return;
		}

		try {
			await verifyMagicLink(token);
			status = 'success';
			// Redirect to profile after short delay
			setTimeout(() => {
				goto('/profile');
			}, 1500);
		} catch (err) {
			status = 'error';
			error = err.message || $t('magicLink.failed');
		}
	});
</script>

<div class="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 text-center">
		{#if status === 'verifying'}
			<div class="mb-4">
				<svg
					class="animate-spin h-12 w-12 text-blue-600 dark:text-blue-400 mx-auto"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
				>
					<circle
						class="opacity-25"
						cx="12"
						cy="12"
						r="10"
						stroke="currentColor"
						stroke-width="4"
					></circle>
					<path
						class="opacity-75"
						fill="currentColor"
						d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
					></path>
				</svg>
			</div>
			<h2 class="text-xl font-semibold text-gray-800 dark:text-white">{$t('magicLink.verifying')}</h2>
			<p class="text-gray-600 dark:text-gray-400 mt-2">{$t('magicLink.pleaseWait')}</p>
		{:else if status === 'success'}
			<div class="mb-4">
				<svg
					class="h-12 w-12 text-green-600 dark:text-green-400 mx-auto"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M5 13l4 4L19 7"
					/>
				</svg>
			</div>
			<h2 class="text-xl font-semibold text-green-800 dark:text-green-400">{$t('magicLink.success')}</h2>
			<p class="text-gray-600 dark:text-gray-400 mt-2">{$t('magicLink.redirecting')}</p>
		{:else}
			<div class="mb-4">
				<svg
					class="h-12 w-12 text-red-600 dark:text-red-400 mx-auto"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					/>
				</svg>
			</div>
			<h2 class="text-xl font-semibold text-red-800 dark:text-red-400">{$t('magicLink.failed')}</h2>
			<p class="text-gray-600 dark:text-gray-400 mt-2">{error}</p>
			<a
				href="/login"
				class="inline-block mt-6 bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 transition-colors"
			>
				{$t('magicLink.backToLogin')}
			</a>
		{/if}
	</div>
</div>
