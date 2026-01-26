<script>
	import { onMount } from 'svelte';
	import { adminListProjects, adminUpdateProject, adminDeleteProject } from '$lib/api';
	import { t, language } from '$lib/stores/language';
	import {
		formatCurrency,
		formatDateShort,
		getStatusColor,
		getProjectTypeColor,
		getSortIcon as baseSortIcon
	} from '$lib/utils';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import Alert from '$lib/components/Alert.svelte';
	import Badge from '$lib/components/Badge.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

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

	// Locale-aware wrappers
	$: locale = $language === 'de' ? 'de-DE' : 'en-US';
	function formatDate(dateString) {
		return formatDateShort(dateString, locale);
	}
	function getSortIconForColumn(column) {
		return baseSortIcon(column, sortBy, sortDir);
	}

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
</script>

<div>
	<h1 class="text-3xl font-bold text-[#304b50] dark:text-white mb-8">{$t('admin.projectManagement')}</h1>

	<Alert type="error" message={error} />
	<Alert type="success" message={success} />

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
			<LoadingSpinner />
		</div>
	{:else if projects.length === 0}
		<EmptyState message={$t('admin.noProjects')} />
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
								{$t('project.title')} {getSortIconForColumn('title')}
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
								{$t('project.type')} {getSortIconForColumn('project_type')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('plan')}
							>
								Plan {getSortIconForColumn('plan')}
							</th>
							<th
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
								on:click={() => toggleSort('status')}
							>
								{$t('admin.status')} {getSortIconForColumn('status')}
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
								{$t('project.createdAt')} {getSortIconForColumn('created_at')}
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
									<Badge type="projectType" value={project.project_type || 'crowdfunding'} />
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm">
									{#if project.plan}
										<div class="font-medium text-[#304b50] dark:text-white capitalize">{project.plan}</div>
										{#if project.provision}
											<div class="text-xs text-gray-500 dark:text-gray-400">{project.provision.toFixed(2).replace('.', ',')}%</div>
										{/if}
									{:else}
										<span class="text-gray-400">-</span>
									{/if}
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
