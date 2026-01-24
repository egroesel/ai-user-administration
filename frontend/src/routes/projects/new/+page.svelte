<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { t } from '$lib/stores/language';
	import { auth } from '$lib/stores/auth';
	import { suggestSlug, createProject, login } from '$lib/api';
	import AuthForm from '$lib/components/AuthForm.svelte';

	const STORAGE_KEY = 'pendingProject';

	let title = '';
	let slug = '';
	let slugEdited = false;
	let shortDescription = '';
	let description = '';
	let fundingGoal = '';
	let imageUrl = '';
	let videoUrl = '';
	let projectType = 'crowdfunding';

	let loading = false;
	let error = null;
	let slugLoading = false;

	// Auth modal state
	let showAuthModal = false;
	let authMode = 'magic';

	// Save form data to localStorage
	function saveFormData() {
		const data = {
			title,
			slug,
			slugEdited,
			shortDescription,
			description,
			fundingGoal,
			imageUrl,
			videoUrl,
			projectType
		};
		localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
	}

	// Load form data from localStorage
	function loadFormData() {
		const saved = localStorage.getItem(STORAGE_KEY);
		if (saved) {
			try {
				const data = JSON.parse(saved);
				title = data.title || '';
				slug = data.slug || '';
				slugEdited = data.slugEdited || false;
				shortDescription = data.shortDescription || '';
				description = data.description || '';
				fundingGoal = data.fundingGoal || '';
				imageUrl = data.imageUrl || '';
				videoUrl = data.videoUrl || '';
				projectType = data.projectType || 'crowdfunding';
				return true;
			} catch (e) {
				console.error('Failed to load saved form data:', e);
			}
		}
		return false;
	}

	// Clear saved form data
	function clearFormData() {
		localStorage.removeItem(STORAGE_KEY);
	}

	// On mount, check if we have saved data and user is now logged in
	onMount(async () => {
		const hasSavedData = loadFormData();

		// If user is authenticated and has saved data, auto-submit
		if ($auth.isAuthenticated && hasSavedData && title.trim() && slug.trim()) {
			await submitProject();
		}
	});

	let debounceTimer;
	async function handleTitleChange() {
		if (slugEdited) return;

		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(async () => {
			if (title.trim()) {
				slugLoading = true;
				try {
					const result = await suggestSlug(title);
					if (!slugEdited) {
						slug = result.slug;
					}
				} catch (e) {
					console.error('Failed to suggest slug:', e);
				} finally {
					slugLoading = false;
				}
			}
		}, 300);
	}

	function handleSlugEdit() {
		slugEdited = true;
	}

	async function handleSubmit() {
		error = null;

		if (!title.trim()) {
			error = $t('project.titleRequired');
			return;
		}

		if (!slug.trim()) {
			error = $t('project.slugRequired');
			return;
		}

		// Check if user is authenticated
		if (!$auth.isAuthenticated) {
			// Save form data before showing auth modal
			saveFormData();
			showAuthModal = true;
			return;
		}

		await submitProject();
	}

	async function submitProject() {
		loading = true;
		error = null;

		try {
			const projectData = {
				title: title.trim(),
				slug: slug.trim(),
				short_description: shortDescription.trim() || null,
				description: description.trim() || null,
				funding_goal: fundingGoal ? parseFloat(fundingGoal) : null,
				image_url: imageUrl.trim() || null,
				video_url: videoUrl.trim() || null,
				project_type: projectType
			};

			const project = await createProject(projectData);
			// Clear saved form data after successful creation
			clearFormData();
			goto(`/projects/${project.slug}`);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	function handleLoginSuccess() {
		showAuthModal = false;
		// Now submit the project
		submitProject();
	}

	async function handleRegisterSuccess(event) {
		// Auto-login after registration and submit
		// The AuthForm dispatches this after successful registration
		// We need to log in the user first
		showAuthModal = false;
		submitProject();
	}

	function handleBeforeMagicLink() {
		// Save form data before sending magic link (user will leave page)
		saveFormData();
	}

	function handleModeChange(event) {
		authMode = event.detail.mode;
	}

	function closeAuthModal() {
		showAuthModal = false;
	}
</script>

<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	<div class="mb-8">
		<a href="/" class="text-[#304b50] dark:text-[#06E481] hover:underline flex items-center">
			<svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			{$t('project.back')}
		</a>
	</div>

	<div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
		<h1 class="text-2xl font-bold text-[#304b50] dark:text-white mb-6">
			{$t('project.create')}
		</h1>

		{#if error}
			<div class="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
				{error}
			</div>
		{/if}

		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			<!-- Project Type -->
			<div>
				<label for="projectType" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.type')}
				</label>
				<div class="grid grid-cols-3 gap-3">
					<button
						type="button"
						on:click={() => projectType = 'crowdfunding'}
						class="px-4 py-3 rounded-lg border-2 transition-colors {projectType === 'crowdfunding' ? 'border-[#06E481] bg-[#06E481]/10' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'}"
					>
						<span class="block text-sm font-medium {projectType === 'crowdfunding' ? 'text-[#06E481]' : 'text-gray-700 dark:text-gray-300'}">
							{$t('project.type.crowdfunding')}
						</span>
					</button>
					<button
						type="button"
						on:click={() => projectType = 'fundraising'}
						class="px-4 py-3 rounded-lg border-2 transition-colors {projectType === 'fundraising' ? 'border-[#FF85FF] bg-[#FF85FF]/10' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'}"
					>
						<span class="block text-sm font-medium {projectType === 'fundraising' ? 'text-[#FF85FF]' : 'text-gray-700 dark:text-gray-300'}">
							{$t('project.type.fundraising')}
						</span>
					</button>
					<button
						type="button"
						on:click={() => projectType = 'private'}
						class="px-4 py-3 rounded-lg border-2 transition-colors {projectType === 'private' ? 'border-[#FFC21C] bg-[#FFC21C]/10' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'}"
					>
						<span class="block text-sm font-medium {projectType === 'private' ? 'text-[#FFC21C]' : 'text-gray-700 dark:text-gray-300'}">
							{$t('project.type.private')}
						</span>
					</button>
				</div>
			</div>

			<!-- Title -->
			<div>
				<label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.title')} *
				</label>
				<input
					type="text"
					id="title"
					bind:value={title}
					on:input={handleTitleChange}
					placeholder={$t('project.titlePlaceholder')}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
					required
				/>
			</div>

			<!-- Slug -->
			<div>
				<label for="slug" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.slug')} *
				</label>
				<div class="relative">
					<input
						type="text"
						id="slug"
						bind:value={slug}
						on:input={handleSlugEdit}
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
						required
					/>
					{#if slugLoading}
						<div class="absolute right-3 top-1/2 -translate-y-1/2">
							<div class="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-[#06E481]"></div>
						</div>
					{/if}
				</div>
				<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
					{$t('project.slugHint')}
				</p>
			</div>

			<!-- Short Description -->
			<div>
				<label for="shortDescription" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.shortDescription')}
				</label>
				<textarea
					id="shortDescription"
					bind:value={shortDescription}
					rows="2"
					maxlength="500"
					placeholder={$t('project.shortDescriptionPlaceholder')}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
				></textarea>
				<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
					{shortDescription.length}/500
				</p>
			</div>

			<!-- Description -->
			<div>
				<label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.description')}
				</label>
				<textarea
					id="description"
					bind:value={description}
					rows="6"
					placeholder={$t('project.descriptionPlaceholder')}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
				></textarea>
			</div>

			<!-- Funding Goal -->
			<div>
				<label for="fundingGoal" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.fundingGoal')} (EUR)
				</label>
				<input
					type="number"
					id="fundingGoal"
					bind:value={fundingGoal}
					min="0"
					step="1"
					placeholder={$t('project.fundingGoalPlaceholder')}
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
				/>
			</div>

			<!-- Image URL -->
			<div>
				<label for="imageUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.imageUrl')}
				</label>
				<input
					type="url"
					id="imageUrl"
					bind:value={imageUrl}
					placeholder="https://..."
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
				/>
			</div>

			<!-- Video URL -->
			<div>
				<label for="videoUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
					{$t('project.videoUrl')}
				</label>
				<input
					type="url"
					id="videoUrl"
					bind:value={videoUrl}
					placeholder="https://..."
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-[#06E481] focus:border-[#06E481] dark:bg-gray-700 dark:text-white"
				/>
			</div>

			<!-- Submit Button -->
			<div class="pt-4">
				<button
					type="submit"
					disabled={loading}
					class="w-full px-4 py-3 font-semibold rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors
						{projectType === 'crowdfunding' ? 'bg-[#06E481] text-[#304b50] hover:bg-[#05b667] focus:ring-[#06E481]' : ''}
						{projectType === 'fundraising' ? 'bg-[#FF85FF] text-white hover:bg-[#e070e0] focus:ring-[#FF85FF]' : ''}
						{projectType === 'private' ? 'bg-[#FFC21C] text-[#304b50] hover:bg-[#e0aa18] focus:ring-[#FFC21C]' : ''}"
				>
					{loading ? $t('project.creating') : $t('project.create')}
				</button>
			</div>
		</form>
	</div>
</div>

<!-- Auth Modal -->
{#if showAuthModal}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 max-w-md w-full max-h-[90vh] overflow-y-auto">
			<div class="flex justify-between items-center mb-6">
				<h2 class="text-2xl font-bold text-[#304b50] dark:text-white">
					{authMode === 'register' ? $t('register.title') : $t('login.title')}
				</h2>
				<button
					on:click={closeAuthModal}
					class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
				>
					<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<AuthForm
				bind:mode={authMode}
				on:loginsuccess={handleLoginSuccess}
				on:registersuccess={handleRegisterSuccess}
				on:beforemagiclink={handleBeforeMagicLink}
				on:modechange={handleModeChange}
			/>
		</div>
	</div>
{/if}
