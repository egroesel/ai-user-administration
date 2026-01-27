<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { isAuthenticated, isAdmin } from '$lib/api';
	import { t } from '$lib/stores/language';

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

	$: currentPath = $page.url.pathname;
</script>

<div class="min-h-[calc(100vh-4rem)] bg-gray-100 dark:bg-gray-900">
	<div class="flex">
		<!-- Sidebar - hidden on mobile -->
		<aside class="hidden md:block w-64 bg-white dark:bg-gray-800 shadow-md min-h-[calc(100vh-4rem)] flex-shrink-0">
			<div class="p-6 border-b border-gray-200 dark:border-gray-700">
				<h2 class="text-xl font-bold text-[#304b50] dark:text-white">{$t('admin.title')}</h2>
			</div>
			<nav class="p-4">
				<ul class="space-y-2">
					<li>
						<a
							href="/admin/projects"
							class="flex items-center px-4 py-2 rounded-md transition-colors {currentPath === '/admin/projects' || currentPath === '/admin'
								? 'bg-[#06E481]/20 dark:bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]'
								: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
						>
							<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
							</svg>
							{$t('admin.projectManagement')}
						</a>
					</li>
					<li>
						<a
							href="/admin/users"
							class="flex items-center px-4 py-2 rounded-md transition-colors {currentPath === '/admin/users'
								? 'bg-[#06E481]/20 dark:bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]'
								: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
						>
							<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
							</svg>
							{$t('admin.userManagement')}
						</a>
					</li>
					<li>
						<a
							href="/admin/system"
							class="flex items-center px-4 py-2 rounded-md transition-colors {currentPath === '/admin/system' || currentPath.startsWith('/admin/system/')
								? 'bg-[#06E481]/20 dark:bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]'
								: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
						>
							<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							{$t('admin.system')}
						</a>
					</li>
				</ul>
			</nav>
		</aside>

		<!-- Main Content -->
		<main class="flex-1 min-w-0 overflow-hidden p-4 md:p-8">
			<!-- Mobile Tab Navigation -->
			<nav class="md:hidden mb-4 -mx-4 px-4 overflow-x-auto">
				<div class="flex gap-2 min-w-max">
					<a
						href="/admin/projects"
						class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors {currentPath === '/admin/projects' || currentPath === '/admin'
							? 'bg-[#06E481] text-[#304b50]'
							: 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'}"
					>
						{$t('admin.projectManagement')}
					</a>
					<a
						href="/admin/users"
						class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors {currentPath === '/admin/users'
							? 'bg-[#06E481] text-[#304b50]'
							: 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'}"
					>
						{$t('admin.userManagement')}
					</a>
					<a
						href="/admin/system"
						class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors {currentPath === '/admin/system' || currentPath.startsWith('/admin/system/')
							? 'bg-[#06E481] text-[#304b50]'
							: 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300'}"
					>
						{$t('admin.system')}
					</a>
				</div>
			</nav>
			<div class="overflow-x-auto">
				<slot />
			</div>
		</main>
	</div>
</div>
