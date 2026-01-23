<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { sendTestEmail, isAuthenticated, isAdmin } from '$lib/api';
	import { t, language } from '$lib/stores/language';

	let email = '';
	let userName = '';
	let emailType = 'test_simple';
	let error = '';
	let success = '';
	let loading = false;

	$: emailTypes = [
		{ value: 'test_simple', label: $t('admin.emailType.testSimple') },
		{ value: 'welcome', label: $t('admin.emailType.welcome') },
		{ value: 'password_reset', label: $t('admin.emailType.passwordReset') },
		{ value: 'account_activated', label: $t('admin.emailType.accountActivated') },
		{ value: 'account_deactivated', label: $t('admin.emailType.accountDeactivated') }
	];

	onMount(() => {
		if (!isAuthenticated()) {
			goto('/login');
			return;
		}

		if (!isAdmin()) {
			goto('/profile');
			return;
		}
	});

	async function handleSendTestEmail() {
		error = '';
		success = '';
		loading = true;

		try {
			const response = await sendTestEmail(email, emailType, userName || null);
			success = response.message;
			email = '';
			userName = '';
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="mb-6">
		<a href="/admin" class="text-blue-600 dark:text-blue-400 hover:underline">&larr; {$t('admin.backToAdmin')}</a>
	</div>

	<h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-8">{$t('admin.emailTest')}</h1>

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

	<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
		<h2 class="text-xl font-semibold text-gray-800 dark:text-white mb-4">{$t('admin.sendTestEmailForm')}</h2>

		<form on:submit|preventDefault={handleSendTestEmail}>
			<div class="mb-4">
				<label for="emailType" class="block text-gray-700 dark:text-gray-300 font-medium mb-2">{$t('admin.emailType')}</label>
				<select
					id="emailType"
					bind:value={emailType}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				>
					{#each emailTypes as type}
						<option value={type.value}>{type.label}</option>
					{/each}
				</select>
			</div>

			<div class="mb-4">
				<label for="email" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
					>{$t('admin.recipientEmail')}</label
				>
				<input
					type="email"
					id="email"
					bind:value={email}
					required
					placeholder="test@example.com"
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				/>
			</div>

			<div class="mb-6">
				<label for="userName" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
					>{$t('admin.nameOptional')}</label
				>
				<input
					type="text"
					id="userName"
					bind:value={userName}
					placeholder={$language === 'de' ? 'Max Mustermann' : 'John Doe'}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
				/>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{$t('admin.nameHint')}</p>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
			>
				{loading ? $t('admin.sending') : $t('admin.sendTestEmail')}
			</button>
		</form>
	</div>

	<div class="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
		<h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-3">{$t('admin.availableEmailTypes')}</h3>

		<div class="space-y-3">
			<div>
				<span class="font-medium text-gray-700 dark:text-gray-300">{$t('admin.emailType.testSimple')}:</span>
				<p class="text-gray-600 dark:text-gray-400 text-sm">{$t('admin.emailType.testSimpleDesc')}</p>
			</div>

			<div>
				<span class="font-medium text-gray-700 dark:text-gray-300">{$t('admin.emailType.welcome')}:</span>
				<p class="text-gray-600 dark:text-gray-400 text-sm">{$t('admin.emailType.welcomeDesc')}</p>
			</div>

			<div>
				<span class="font-medium text-gray-700 dark:text-gray-300">{$t('admin.emailType.passwordReset')}:</span>
				<p class="text-gray-600 dark:text-gray-400 text-sm">{$t('admin.emailType.passwordResetDesc')}</p>
			</div>

			<div>
				<span class="font-medium text-gray-700 dark:text-gray-300">{$t('admin.emailType.accountActivated')}:</span>
				<p class="text-gray-600 dark:text-gray-400 text-sm">{$t('admin.emailType.accountActivatedDesc')}</p>
			</div>

			<div>
				<span class="font-medium text-gray-700 dark:text-gray-300">{$t('admin.emailType.accountDeactivated')}:</span>
				<p class="text-gray-600 dark:text-gray-400 text-sm">{$t('admin.emailType.accountDeactivatedDesc')}</p>
			</div>
		</div>
	</div>
</div>
