<script>
	import { goto } from '$app/navigation';
	import { login, requestMagicLink } from '$lib/api';
	import { t } from '$lib/stores/language';

	let email = '';
	let password = '';
	let twoFactorCode = '';
	let error = '';
	let success = '';
	let loading = false;
	let needs2FA = false;
	let loginMethod = 'magic'; // 'magic' or 'password'

	async function handleMagicLink() {
		error = '';
		success = '';
		loading = true;

		try {
			await requestMagicLink(email);
			success = $t('login.magicLinkSent');
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}

	async function handlePasswordLogin() {
		error = '';
		success = '';
		loading = true;

		try {
			await login(email, password, needs2FA ? twoFactorCode : null);
			goto('/profile');
		} catch (err) {
			if (err.message.includes('Two-factor authentication code required')) {
				needs2FA = true;
				error = '';
			} else {
				error = err.message;
			}
		} finally {
			loading = false;
		}
	}

	function handleSubmit() {
		if (loginMethod === 'magic') {
			handleMagicLink();
		} else {
			handlePasswordLogin();
		}
	}
</script>

<div class="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
		<h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">{$t('login.title')}</h2>

		{#if error}
			<div class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-4">
				{error}
			</div>
		{/if}

		{#if success}
			<div class="bg-green-100 dark:bg-green-900/30 border border-green-400 dark:border-green-600 text-green-700 dark:text-green-400 px-4 py-3 rounded mb-4">
				{success}
			</div>
		{/if}

		<!-- Login Method Tabs -->
		<div class="flex mb-6 border-b border-gray-200 dark:border-gray-600">
			<button
				type="button"
				on:click={() => (loginMethod = 'magic')}
				class="flex-1 py-2 text-center border-b-2 transition-colors {loginMethod === 'magic'
					? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
					: 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
			>
				{$t('login.magicLink')}
			</button>
			<button
				type="button"
				on:click={() => (loginMethod = 'password')}
				class="flex-1 py-2 text-center border-b-2 transition-colors {loginMethod === 'password'
					? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
					: 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
			>
				{$t('login.password')}
			</button>
		</div>

		<form on:submit|preventDefault={handleSubmit}>
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

			{#if loginMethod === 'password'}
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

				{#if needs2FA}
					<div class="mb-4">
						<label for="twoFactorCode" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
							>{$t('login.2faCode')}</label
						>
						<input
							type="text"
							id="twoFactorCode"
							bind:value={twoFactorCode}
							required
							placeholder="123456"
							class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
						/>
					</div>
				{/if}
			{/if}

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
			>
				{#if loading}
					{loginMethod === 'magic' ? $t('login.sendingLink') : $t('login.submitting')}
				{:else}
					{loginMethod === 'magic' ? $t('login.sendLink') : $t('login.submit')}
				{/if}
			</button>
		</form>

		{#if loginMethod === 'magic'}
			<p class="mt-4 text-sm text-gray-600 dark:text-gray-400 text-center">
				{$t('login.magicLinkInfo')}
			</p>
		{/if}

		<div class="mt-6 text-center space-y-2">
			<p class="text-gray-600 dark:text-gray-400">
				{$t('login.noAccount')}
				<a href="/register" class="text-blue-600 dark:text-blue-400 hover:underline">{$t('nav.register')}</a>
			</p>
			{#if loginMethod === 'password'}
				<p>
					<a href="/forgot-password" class="text-blue-600 dark:text-blue-400 hover:underline text-sm"
						>{$t('login.forgotPassword')}</a
					>
				</p>
			{/if}
		</div>
	</div>
</div>
