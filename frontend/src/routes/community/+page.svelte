<script>
	import { onMount } from 'svelte';
	import { t } from '$lib/stores/language';
	import { getAllStarters } from '$lib/api';

	let starters = [];
	let loading = true;
	let error = null;

	onMount(async () => {
		try {
			starters = await getAllStarters(0, 100);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function formatCurrency(amount) {
		return new Intl.NumberFormat('de-DE', {
			style: 'currency',
			currency: 'EUR',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(amount || 0);
	}

	function getInitials(name) {
		if (!name) return '?';
		return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
	}

	function formatProjectCount(count) {
		if (count === 1) {
			return $t('community.projectCount').split('|')[0].trim().replace('{count}', count);
		}
		return $t('community.projectCount').split('|')[1]?.trim().replace('{count}', count) || `${count} Projekte`;
	}
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="text-center mb-12">
		<h1 class="text-3xl font-bold text-[#304b50] dark:text-white mb-4">
			{$t('community.title')}
		</h1>
		<p class="text-gray-600 dark:text-gray-400 text-lg">
			{$t('community.subtitle')}
		</p>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-300 border-t-[#06E481]"></div>
			<p class="mt-4 text-gray-600 dark:text-gray-400">{$t('common.loading')}</p>
		</div>
	{:else if error}
		<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
			{error}
		</div>
	{:else if starters.length === 0}
		<div class="text-center py-12">
			<svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
			</svg>
			<p class="text-xl text-gray-500 dark:text-gray-400">{$t('community.noStarters')}</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each starters as starter}
				<a href="/profile/{starter.profile_slug}" class="group">
					<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
						<div class="flex items-center mb-4">
							<div class="w-16 h-16 rounded-full bg-gradient-to-br from-[#304b50] to-[#06E481] flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
								<span class="text-xl font-bold text-white">
									{getInitials(starter.full_name)}
								</span>
							</div>
							<div class="ml-4">
								<h3 class="font-semibold text-[#304b50] dark:text-white group-hover:text-[#06E481] transition-colors">
									{starter.full_name}
								</h3>
								<div class="flex flex-wrap gap-1 mt-1">
									{#if starter.project_count >= 3}
										<span class="inline-block px-2 py-0.5 bg-[#FFC21C]/20 text-[#FFC21C] text-xs font-medium rounded-full">
											{$t('profile.serialStarter')}
										</span>
									{/if}
									<span class="inline-block px-2 py-0.5 bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481] text-xs font-medium rounded-full">
										{$t('profile.starter')}
									</span>
								</div>
							</div>
						</div>
						<div class="border-t border-gray-200 dark:border-gray-700 pt-4">
							<div class="flex justify-between text-sm">
								<span class="text-gray-500 dark:text-gray-400">
									{formatProjectCount(starter.project_count)}
								</span>
								{#if starter.total_funding_raised > 0}
									<span class="text-[#06E481] font-medium">
										{formatCurrency(starter.total_funding_raised)}
									</span>
								{/if}
							</div>
						</div>
					</div>
				</a>
			{/each}
		</div>
	{/if}
</div>
