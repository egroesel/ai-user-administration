<script>
	import { goto } from '$app/navigation';
	import { register } from '$lib/api';
	import { t } from '$lib/stores/language';

	let email = '';
	let password = '';
	let confirmPassword = '';
	let fullName = '';
	let error = '';
	let loading = false;

	async function handleRegister() {
		error = '';

		if (password !== confirmPassword) {
			error = $t('register.passwordMismatch');
			return;
		}

		if (password.length < 8) {
			error = $t('register.passwordTooShort');
			return;
		}

		loading = true;

		try {
			await register(email, password, fullName);
			goto('/login');
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
		<h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">{$t('register.title')}</h2>

		{#if error}
			<div class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-4">
				{error}
			</div>
		{/if}

		<form on:submit|preventDefault={handleRegister}>
			<div class="mb-4">
				<label for="email" class="block text-gray-700 dark:text-gray-300 font-medium mb-2">{$t('login.email')}</label>
				<input
					type="email"
					id="email"
					bind:value={email}
					required
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				/>
			</div>

			<div class="mb-4">
				<label for="fullName" class="block text-gray-700 dark:text-gray-300 font-medium mb-2">{$t('register.fullName')}</label>
				<input
					type="text"
					id="fullName"
					bind:value={fullName}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				/>
			</div>

			<div class="mb-4">
				<label for="password" class="block text-gray-700 dark:text-gray-300 font-medium mb-2">{$t('login.password')}</label>
				<input
					type="password"
					id="password"
					bind:value={password}
					required
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				/>
			</div>

			<div class="mb-6">
				<label for="confirmPassword" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
					>{$t('register.confirmPassword')}</label
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
				{loading ? $t('register.submitting') : $t('register.submit')}
			</button>
		</form>

		<div class="mt-6 text-center">
			<p class="text-gray-600 dark:text-gray-400">
				{$t('register.hasAccount')}
				<a href="/login" class="text-blue-600 dark:text-blue-400 hover:underline">{$t('nav.login')}</a>
			</p>
		</div>
	</div>
</div>
