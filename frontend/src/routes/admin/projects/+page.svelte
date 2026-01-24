<script>
	import { onMount } from 'svelte';
	import { adminListProjects, adminUpdateProject, adminDeleteProject } from '$lib/api';
	import { t, language } from '$lib/stores/language';

	let projects = [];
	let loading = true;
	let error = '';
	let success = '';
	let sortBy = 'created_at';
	let sortDir = 'desc';
	let statusFilter = '';
	let projectTypeFilter = '';

	const statuses = ['draft', 'submitted', 'verified', 'financing', 'ended_success', 'ended_failed', 'rejected'];
	const projectTypes = ['crowdfunding', 'fundraising', 'private'];

	onMount(async () => {
		await loadProjects();
	});

	async function loadProjects() {
		loading = true;
		error = '';
		try {
			projects = await adminListProjects(statusFilter || null, projectTypeFilter || null);
			sortProjects();
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}

	function sortProjects() {
		projects = [...projects].sort((a, b) => {
			let aVal = a[sortBy];
			let bVal = b[sortBy];

			if (sortBy === 'created_at' || sortBy === 'submitted_at') {
				aVal = aVal ? new Date(aVal).getTime() : 0;
				bVal = bVal ? new Date(bVal).getTime() : 0;
			} else if (typeof aVal === 'string') {
				aVal = aVal?.toLowerCase() || '';
				bVal = bVal?.toLowerCase() || '';
			}

			if (sortDir === 'asc') {
				return aVal > bVal ? 1 : -1;
			} else {
				return aVal < bVal ? 1 : -1;
			}
		});
	}

	function toggleSort(column) {
		if (sortBy === column) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortBy = column;
			sortDir = 'desc';
		}
		sortProjects();
	}

	async function handleStatusChange(projectId, newStatus) {
		error = '';
		success = '';
		try {
			await adminUpdateProject(projectId, { status: newStatus });
			success = $t('admin.projectStatusUpdated');
			await loadProjects();
		} catch (err) {
			error = err.message;
		}
	}

	async function handleDeleteProject(projectId, title) {
		const confirmMsg = $t('admin.confirmDeleteProject').replace('{title}', title);
		if (!confirm(confirmMsg)) {
			return;
		}

		error = '';
		success = '';
		try {
			await adminDeleteProject(projectId);
			success = $t('admin.projectDeleted');
			await loadProjects();
		} catch (err) {
			error = err.message;
		}
	}

	function formatDate(dateString) {
		if (!dateString) return '-';
		return new Date(dateString).toLocaleDateString($language === 'de' ? 'de-DE' : 'en-US');
	}

	function formatCurrency(amount) {
		return new Intl.NumberFormat($language === 'de' ? 'de-DE' : 'en-US', {
			style: 'currency',
			currency: 'EUR',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(amount || 0);
	}

	function getStatusColor(status) {
		switch (status) {
			case 'draft':
				return 'bg-gray-100 dark:bg-gray-700 text-[#304b50] dark:text-gray-300';
			case 'submitted':
				return 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-400';
			case 'verified':
				return 'bg-[#06E481]/20 dark:bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]';
			case 'financing':
				return 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-400';
			case 'ended_success':
				return 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-400';
			case 'ended_failed':
				return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-400';
			case 'rejected':
				return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-400';
			default:
				return 'bg-gray-100 dark:bg-gray-700 text-[#304b50] dark:text-gray-300';
		}
	}

	function getSortIcon(column) {
		if (sortBy !== column) return '↕';
		return sortDir === 'asc' ? '↑' : '↓';
	}

	function getProjectTypeColor(type) {
		switch (type) {
			case 'crowdfunding':
				return 'bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]';
			case 'fundraising':
				return 'bg-[#FF85FF]/20 text-[#FF85FF]';
			case 'private':
				return 'bg-[#FFC21C]/20 text-[#FFC21C]';
			default:
				return 'bg-gray-100 dark:bg-gray-700 text-[#304b50] dark:text-gray-300';
		}
	}
</script>

<div>
	<h1 class="text-3xl font-bold text-[#304b50] dark:text-white mb-8">{$t('admin.projectManagement')}</h1>

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

	<!-- Filters -->
	<div class="mb-6 flex flex-wrap gap-3 items-center">
		<select
			bind:value={statusFilter}
			on:change={loadProjects}
			class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#06E481] bg-white dark:bg-gray-700 text-[#304b50] dark:text-white"
		>
			<option value="">{$t('admin.allStatuses')}</option>
			{#each statuses as status}
				<option value={status}>{$t(`project.status.${status}`)}</option>
			{/each}
		</select>
		<select
			bind:value={projectTypeFilter}
			on:change={loadProjects}
			class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-[#06E481] bg-white dark:bg-gray-700 text-[#304b50] dark:text-white"
			>
				<option value="">{$t('admin.allTypes')}</option>
				{#each projectTypes as pType}
					<option value={pType}>{$t(`project.type.${pType}`)}</option>
				{/each}
			</select>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<p class="text-gray-600 dark:text-gray-400">{$t('common.loading')}</p>
		</div>
	{:else if projects.length === 0}
		<div class="text-center py-12 bg-gray-100 dark:bg-gray-800 rounded-lg">
			<p class="text-gray-600 dark:text-gray-400">{$t('admin.noProjects')}</p>
		</div>
	{:else}
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
					<thead class="bg-gray-50 dark:bg-gray-700">
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('title')}
							>
								{$t('project.title')} {getSortIcon('title')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('owner.email')}
							>
								{$t('project.owner')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('project_type')}
							>
								{$t('project.type')} {getSortIcon('project_type')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('status')}
							>
								{$t('admin.status')} {getSortIcon('status')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('project.funding')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('created_at')}
							>
								{$t('project.createdAt')} {getSortIcon('created_at')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
							>
								{$t('admin.actions')}
							</th>
						</tr>
					</thead>
					<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
						{#each projects as project}
							<tr>
								<td class="px-6 py-4 whitespace-nowrap">
									<a
										href="/projects/{project.slug}"
										class="text-[#304b50] dark:text-[#06E481] hover:underline font-medium"
									>
										{project.title}
									</a>
									<div class="text-xs text-gray-500 dark:text-gray-400">{project.slug}</div>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-[#304b50] dark:text-gray-100">
									{project.owner?.email || '-'}
									{#if project.owner?.full_name}
										<div class="text-xs text-gray-500 dark:text-gray-400">{project.owner.full_name}</div>
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class="text-xs px-2 py-1 rounded-full font-medium {getProjectTypeColor(project.project_type)}">
										{$t(`project.type.${project.project_type || 'crowdfunding'}`)}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<select
										value={project.status}
										on:change={(e) => handleStatusChange(project.id, e.target.value)}
										class="text-xs px-2 py-1 rounded border-0 {getStatusColor(project.status)} cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#06E481]"
									>
										{#each statuses as status}
											<option value={status}>{$t(`project.status.${status}`)}</option>
										{/each}
									</select>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-[#304b50] dark:text-gray-100">
									{#if project.funding_goal}
										<div>{formatCurrency(project.funding_current)}</div>
										<div class="text-xs text-gray-500 dark:text-gray-400">
											/ {formatCurrency(project.funding_goal)}
										</div>
									{:else}
										-
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
									{formatDate(project.created_at)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
									<a
										href="/projects/{project.slug}"
										class="text-[#304b50] dark:text-[#06E481] hover:text-[#1d2d30] dark:hover:text-[#33f79f]"
									>
										{$t('admin.view')}
									</a>
									<button
										on:click={() => handleDeleteProject(project.id, project.title)}
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
			<p>{$t('admin.totalProjectCount').replace('{count}', projects.length)}</p>
		</div>
	{/if}
</div>
