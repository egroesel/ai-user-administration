<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { confirmPasswordReset } from '$lib/api';
	import { t } from '$lib/stores/language';

	let token = '';
	let newPassword = '';
	let confirmPassword = '';
	let error = '';
	let success = false;
	let loading = false;

	onMount(() => {
		token = $page.url.searchParams.get('token') || '';
		if (!token) {
			error = $t('passwordReset.invalidToken');
		}
	});

	async function handleSubmit() {
		error = '';

		if (newPassword !== confirmPassword) {
			error = $t('register.passwordMismatch');
			return;
		}

		if (newPassword.length < 8) {
			error = $t('register.passwordTooShort');
			return;
		}

		loading = true;

		try {
			await confirmPasswordReset(token, newPassword);
			success = true;
			setTimeout(() => goto('/login'), 2000);
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
		<h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">{$t('passwordReset.title')}</h2>

		{#if error}
			<div class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-4">
				{error}
			</div>
		{/if}

		{#if success}
			<div class="bg-green-100 dark:bg-green-900/30 border border-green-400 dark:border-green-600 text-green-700 dark:text-green-400 px-4 py-3 rounded mb-4">
				{$t('passwordReset.successRedirect')}
			</div>
		{:else if token}
			<form on:submit|preventDefault={handleSubmit}>
				<div class="mb-4">
					<label for="newPassword" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
						>{$t('passwordReset.newPassword')}</label
					>
					<input
						type="password"
						id="newPassword"
						bind:value={newPassword}
						required
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
					/>
				</div>

				<div class="mb-6">
					<label for="confirmPassword" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
						>{$t('passwordReset.confirm')}</label
					>
					<input
						type="password"
						id="confirmPassword"
						bind:value={confirmPassword}
						required
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
				>
					{loading ? $t('profile.saving') : $t('passwordReset.submit')}
				</button>
			</form>
		{/if}

		<div class="mt-6 text-center">
			<a href="/login" class="text-blue-600 dark:text-blue-400 hover:underline">{$t('passwordReset.backToLogin')}</a>
		</div>
	</div>
</div>
