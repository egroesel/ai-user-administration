<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { sendTestEmail, isAuthenticated, isAdmin } from '$lib/api';

	let email = '';
	let userName = '';
	let emailType = 'test_simple';
	let error = '';
	let success = '';
	let loading = false;

	const emailTypes = [
		{ value: 'test_simple', label: 'Einfache Test-Email' },
		{ value: 'welcome', label: 'Willkommens-Email' },
		{ value: 'password_reset', label: 'Passwort zurücksetzen' },
		{ value: 'account_activated', label: 'Account aktiviert' },
		{ value: 'account_deactivated', label: 'Account deaktiviert' }
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
		<a href="/admin" class="text-blue-600 hover:underline">&larr; Zurück zur Admin-Übersicht</a>
	</div>

	<h1 class="text-3xl font-bold text-gray-800 mb-8">Email-Test</h1>

	{#if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
			{error}
		</div>
	{/if}

	{#if success}
		<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
			{success}
		</div>
	{/if}

	<div class="bg-white rounded-lg shadow-md p-6">
		<h2 class="text-xl font-semibold text-gray-800 mb-4">Test-Email versenden</h2>

		<form on:submit|preventDefault={handleSendTestEmail}>
			<div class="mb-4">
				<label for="emailType" class="block text-gray-700 font-medium mb-2">Email-Typ</label>
				<select
					id="emailType"
					bind:value={emailType}
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					{#each emailTypes as type}
						<option value={type.value}>{type.label}</option>
					{/each}
				</select>
			</div>

			<div class="mb-4">
				<label for="email" class="block text-gray-700 font-medium mb-2"
					>Empfänger E-Mail-Adresse</label
				>
				<input
					type="email"
					id="email"
					bind:value={email}
					required
					placeholder="test@example.com"
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div class="mb-6">
				<label for="userName" class="block text-gray-700 font-medium mb-2"
					>Name (optional)</label
				>
				<input
					type="text"
					id="userName"
					bind:value={userName}
					placeholder="Max Mustermann"
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
				<p class="text-sm text-gray-500 mt-1">Wird in der Email als Anrede verwendet</p>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
			>
				{loading ? 'Wird gesendet...' : 'Test-Email senden'}
			</button>
		</form>
	</div>

	<div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
		<h3 class="text-lg font-semibold text-gray-800 mb-3">Verfügbare Email-Typen</h3>

		<div class="space-y-3">
			<div>
				<span class="font-medium text-gray-700">Einfache Test-Email:</span>
				<p class="text-gray-600 text-sm">Eine einfache Test-Email zum Prüfen der Konfiguration</p>
			</div>

			<div>
				<span class="font-medium text-gray-700">Willkommens-Email:</span>
				<p class="text-gray-600 text-sm">
					Email, die an neue Benutzer nach der Registrierung gesendet wird
				</p>
			</div>

			<div>
				<span class="font-medium text-gray-700">Passwort zurücksetzen:</span>
				<p class="text-gray-600 text-sm">
					Email mit Link zum Zurücksetzen des Passworts (Test-Token)
				</p>
			</div>

			<div>
				<span class="font-medium text-gray-700">Account aktiviert:</span>
				<p class="text-gray-600 text-sm">
					Benachrichtigung, wenn ein Account aktiviert wurde
				</p>
			</div>

			<div>
				<span class="font-medium text-gray-700">Account deaktiviert:</span>
				<p class="text-gray-600 text-sm">
					Benachrichtigung, wenn ein Account deaktiviert wurde
				</p>
			</div>
		</div>
	</div>
</div>
