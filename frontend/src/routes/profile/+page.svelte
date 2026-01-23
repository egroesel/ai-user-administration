<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getCurrentUser, updateProfile, setup2FA, verify2FA, disable2FA, isAuthenticated } from '$lib/api';
	import { t } from '$lib/stores/language';

	let user = null;
	let loading = true;
	let error = '';
	let success = '';

	let fullName = '';
	let newPassword = '';
	let confirmPassword = '';

	let twoFactorSecret = '';
	let twoFactorQRCode = '';
	let twoFactorVerifyCode = '';
	let show2FASetup = false;

	onMount(async () => {
		if (!isAuthenticated()) {
			goto('/login');
			return;
		}

		try {
			user = await getCurrentUser();
			fullName = user.full_name || '';
		} catch (err) {
			error = err.message;
			goto('/login');
		} finally {
			loading = false;
		}
	});

	async function handleUpdateProfile() {
		error = '';
		success = '';

		if (newPassword && newPassword !== confirmPassword) {
			error = $t('register.passwordMismatch');
			return;
		}

		try {
			const updateData = { full_name: fullName };
			if (newPassword) {
				updateData.password = newPassword;
			}

			user = await updateProfile(updateData);
			success = $t('profile.saved');
			newPassword = '';
			confirmPassword = '';
		} catch (err) {
			error = err.message;
		}
	}

	async function handleSetup2FA() {
		error = '';
		try {
			const response = await setup2FA();
			twoFactorSecret = response.secret;
			twoFactorQRCode = response.qr_code_url;
			show2FASetup = true;
		} catch (err) {
			error = err.message;
		}
	}

	async function handleVerify2FA() {
		error = '';
		success = '';
		try {
			await verify2FA(twoFactorVerifyCode);
			success = $t('profile.2faActivated');
			show2FASetup = false;
			user.two_factor_enabled = true;
			twoFactorVerifyCode = '';
		} catch (err) {
			error = err.message;
		}
	}

	async function handleDisable2FA() {
		error = '';
		success = '';
		try {
			await disable2FA(twoFactorVerifyCode);
			success = $t('profile.2faDeactivated');
			user.two_factor_enabled = false;
			twoFactorVerifyCode = '';
		} catch (err) {
			error = err.message;
		}
	}
</script>

{#if loading}
	<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
		<p class="text-center text-gray-600 dark:text-gray-400">{$t('common.loading')}</p>
	</div>
{:else if user}
	<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
		<h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-8">{$t('profile.title')}</h1>

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

		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
			<h2 class="text-xl font-semibold text-gray-800 dark:text-white mb-4">{$t('profile.accountInfo')}</h2>
			<div class="space-y-3">
				<div>
					<span class="font-medium text-gray-700 dark:text-gray-300">{$t('profile.email')}:</span>
					<span class="text-gray-600 dark:text-gray-400 ml-2">{user.email}</span>
				</div>
				<div>
					<span class="font-medium text-gray-700 dark:text-gray-300">{$t('profile.status')}:</span>
					{#if user.is_active}
						<span class="ml-2 inline-block bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-400 px-2 py-1 rounded text-sm"
							>{$t('profile.active')}</span
						>
					{:else}
						<span class="ml-2 inline-block bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-400 px-2 py-1 rounded text-sm"
							>{$t('profile.inactive')}</span
						>
					{/if}
				</div>
				<div>
					<span class="font-medium text-gray-700 dark:text-gray-300">{$t('profile.role')}:</span>
					{#if user.is_admin}
						<span class="ml-2 inline-block bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-400 px-2 py-1 rounded text-sm"
							>{$t('profile.admin')}</span
						>
					{:else}
						<span class="ml-2 inline-block bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 px-2 py-1 rounded text-sm"
							>{$t('profile.user')}</span
						>
					{/if}
				</div>
			</div>
		</div>

		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
			<h2 class="text-xl font-semibold text-gray-800 dark:text-white mb-4">{$t('profile.editProfile')}</h2>

			<form on:submit|preventDefault={handleUpdateProfile}>
				<div class="mb-4">
					<label for="fullName" class="block text-gray-700 dark:text-gray-300 font-medium mb-2">{$t('profile.fullName')}</label>
					<input
						type="text"
						id="fullName"
						bind:value={fullName}
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
					/>
				</div>

				<div class="mb-4">
					<label for="newPassword" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
						>{$t('profile.newPassword')}</label
					>
					<input
						type="password"
						id="newPassword"
						bind:value={newPassword}
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
					/>
				</div>

				{#if newPassword}
					<div class="mb-6">
						<label for="confirmPassword" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
							>{$t('register.confirmPassword')}</label
						>
						<input
							type="password"
							id="confirmPassword"
							bind:value={confirmPassword}
							class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
						/>
					</div>
				{/if}

				<button
					type="submit"
					class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
				>
					{$t('profile.updateProfile')}
				</button>
			</form>
		</div>

		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
			<h2 class="text-xl font-semibold text-gray-800 dark:text-white mb-4">{$t('profile.2fa')}</h2>

			{#if user.two_factor_enabled}
				<div class="mb-4">
					<p class="text-green-600 dark:text-green-400 mb-4">{$t('profile.2faEnabled')}</p>
					<div class="mb-4">
						<label for="disableCode" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
							>{$t('profile.enterDisableCode')}</label
						>
						<input
							type="text"
							id="disableCode"
							bind:value={twoFactorVerifyCode}
							placeholder="123456"
							class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
						/>
					</div>
					<button
						on:click={handleDisable2FA}
						class="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
					>
						{$t('profile.disable2fa')}
					</button>
				</div>
			{:else}
				{#if !show2FASetup}
					<p class="text-gray-600 dark:text-gray-400 mb-4">{$t('profile.2faDisabled')}</p>
					<button
						on:click={handleSetup2FA}
						class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
					>
						{$t('profile.2faSetup')}
					</button>
				{:else}
					<div class="space-y-4">
						<p class="text-gray-700 dark:text-gray-300">{$t('profile.scanQRCode')}</p>
						{#if twoFactorQRCode}
							<img src={twoFactorQRCode} alt="QR Code" class="mx-auto" />
						{/if}
						<p class="text-sm text-gray-600 dark:text-gray-400">{$t('profile.manualCode')}</p>
						<p class="font-mono text-sm bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 p-2 rounded">{twoFactorSecret}</p>

						<div class="mb-4">
							<label for="verifyCode" class="block text-gray-700 dark:text-gray-300 font-medium mb-2"
								>{$t('profile.enterVerifyCode')}</label
							>
							<input
								type="text"
								id="verifyCode"
								bind:value={twoFactorVerifyCode}
								placeholder="123456"
								class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
							/>
						</div>

						<button
							on:click={handleVerify2FA}
							class="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
						>
							{$t('profile.enable2fa')}
						</button>
						<button
							on:click={() => (show2FASetup = false)}
							class="ml-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
						>
							{$t('common.cancel')}
						</button>
					</div>
				{/if}
			{/if}
		</div>
	</div>
{/if}
