<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { listUsers, updateUser, deleteUser, isAuthenticated, isAdmin } from '$lib/api';
	import { t, language } from '$lib/stores/language';

	let users = [];
	let loading = true;
	let error = '';
	let success = '';

	onMount(async () => {
		if (!isAuthenticated()) {
			goto('/login');
			return;
		}

		if (!isAdmin()) {
			goto('/profile');
			return;
		}

		await loadUsers();
	});

	async function loadUsers() {
		loading = true;
		error = '';
		try {
			users = await listUsers();
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}

	async function toggleActive(userId, currentStatus) {
		error = '';
		success = '';
		try {
			await updateUser(userId, { is_active: !currentStatus });
			success = $t('admin.userStatusUpdated');
			await loadUsers();
		} catch (err) {
			error = err.message;
		}
	}

	async function toggleAdmin(userId, currentStatus) {
		error = '';
		success = '';
		try {
			await updateUser(userId, { is_admin: !currentStatus });
			success = $t('admin.adminStatusUpdated');
			await loadUsers();
		} catch (err) {
			error = err.message;
		}
	}

	async function handleDeleteUser(userId, email) {
		const confirmMsg = $t('admin.confirmDeleteUser').replace('{email}', email);
		if (!confirm(confirmMsg)) {
			return;
		}

		error = '';
		success = '';
		try {
			await deleteUser(userId);
			success = $t('admin.userDeleted');
			await loadUsers();
		} catch (err) {
			error = err.message;
		}
	}

	function formatDate(dateString) {
		return new Date(dateString).toLocaleDateString($language === 'de' ? 'de-DE' : 'en-US');
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="flex justify-between items-center mb-8">
		<h1 class="text-3xl font-bold text-gray-800 dark:text-white">{$t('admin.title')}</h1>
		<a
			href="/admin/email-test"
			class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
		>
			{$t('admin.emailTest')}
		</a>
	</div>

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

	{#if loading}
		<div class="text-center py-12">
			<p class="text-gray-600 dark:text-gray-400">{$t('common.loading')}</p>
		</div>
	{:else}
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
			<div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
				<h2 class="text-xl font-semibold text-gray-800 dark:text-white">{$t('admin.userManagement')}</h2>
			</div>

			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
					<thead class="bg-gray-50 dark:bg-gray-700">
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.email')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.name')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.status')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.role')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.2fa')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.created')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.actions')}
							</th>
						</tr>
					</thead>
					<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
						{#each users as user}
							<tr>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
									{user.email}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
									{user.full_name || '-'}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									{#if user.is_active}
										<span class="inline-block bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-400 px-2 py-1 rounded text-xs"
											>{$t('admin.active')}</span
										>
									{:else}
										<span class="inline-block bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-400 px-2 py-1 rounded text-xs"
											>{$t('admin.inactive')}</span
										>
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									{#if user.is_admin}
										<span class="inline-block bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-400 px-2 py-1 rounded text-xs"
											>{$t('admin.admin')}</span
										>
									{:else}
										<span class="inline-block bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 px-2 py-1 rounded text-xs"
											>{$t('admin.user')}</span
										>
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
									{user.two_factor_enabled ? '✓' : '-'}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
									{formatDate(user.created_at)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
									<button
										on:click={() => toggleActive(user.id, user.is_active)}
										class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
									>
										{user.is_active ? $t('admin.deactivate') : $t('admin.activate')}
									</button>
									<button
										on:click={() => toggleAdmin(user.id, user.is_admin)}
										class="text-purple-600 dark:text-purple-400 hover:text-purple-900 dark:hover:text-purple-300"
									>
										{user.is_admin ? $t('admin.revokeAdmin') : $t('admin.makeAdmin')}
									</button>
									<button
										on:click={() => handleDeleteUser(user.id, user.email)}
										class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
									>
										{$t('admin.delete')}
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<div class="mt-6 text-gray-600 dark:text-gray-400">
			<p>{$t('admin.totalCount').replace('{count}', users.length)}</p>
		</div>
	{/if}
</div>
