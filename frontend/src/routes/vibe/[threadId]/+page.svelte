<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount, afterUpdate } from 'svelte';
	import { aiChat } from '$lib/stores/aiChat';
	import { auth } from '$lib/stores/auth';
	import { t } from '$lib/stores/language';
	import { generateAIDraft, updateAIDraft, convertAIDraft, claimAIThread } from '$lib/api';

	let prompt = '';
	let messagesContainer;
	let draft = null;
	let generatingDraft = false;
	let convertingProject = false;
	let draftError = null;
	let savingField = null;

	// Edit values for draft fields
	let editValues = {};
	let editingField = null;

	$: threadId = $page.params.threadId;
	$: messages = $aiChat.messages;
	$: loading = $aiChat.loading;
	$: canCreateProject = $aiChat.canCreateProject;
	$: requiresLogin = $aiChat.requiresLogin;
	$: settings = $aiChat.settings;
	$: messageCount = $aiChat.messageCount;

	// Translate backend error messages
	function translateError(errorMessage) {
		const errorMap = {
			'Message limit reached. Please log in to continue.': 'vibe.error.messageLimitReached',
			'Not authorized': 'vibe.error.notAuthorized',
			'Not authorized to view this draft': 'vibe.error.notAuthorized',
			'Thread not found': 'vibe.error.threadNotFound',
			'Draft not found': 'vibe.error.draftNotFound',
			'AI Coach is not configured': 'vibe.error.aiNotConfigured',
			'Draft already converted': 'vibe.error.alreadyConverted',
			'Draft must have a title': 'vibe.error.titleRequired'
		};

		// Check for draft limit message (contains variable number)
		if (errorMessage && errorMessage.includes('Anonymous users can only generate')) {
			return $t('vibe.error.draftLimitReached');
		}

		// Check for min messages error
		if (errorMessage && errorMessage.includes('Need at least')) {
			return $t('vibe.error.needMoreMessages');
		}

		const translationKey = errorMap[errorMessage];
		return translationKey ? $t(translationKey) : errorMessage;
	}

	onMount(async () => {
		// Reset draft state when loading a new thread
		draft = null;
		draftError = null;
		editingField = null;
		editValues = {};

		if (threadId) {
			try {
				await aiChat.loadThread(threadId);
			} catch (e) {
				// Thread not found, redirect to vibe landing
				goto('/vibe');
			}
		}
	});

	afterUpdate(() => {
		// Auto-scroll to bottom when new messages arrive
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	});

	async function handleSubmit() {
		if (!prompt.trim() || loading) return;

		const message = prompt.trim();
		prompt = '';

		try {
			await aiChat.sendMessage(message);
		} catch (e) {
			// Error is handled in store
		}
	}

	function handleKeydown(e) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	}

	function initEditValues() {
		if (draft) {
			editValues = {
				title: draft.title || '',
				short_description: draft.short_description || '',
				description: draft.description || '',
				funding_goal: draft.funding_goal || '',
				project_type: draft.project_type || 'crowdfunding',
				plan: draft.plan || 'basic'
			};
		}
	}

	async function handleGenerateDraft() {
		generatingDraft = true;
		draftError = null;

		try {
			// If logged in, claim the thread first
			if ($auth.isAuthenticated) {
				await claimAIThread(threadId).catch(() => {
					// Already claimed, ignore error
				});
			}

			// Get session_id for anonymous users
			const sessionId = $auth.isAuthenticated ? null : aiChat.getSessionId();
			draft = await generateAIDraft(threadId, sessionId);
			initEditValues();
		} catch (e) {
			draftError = e.message;
		} finally {
			generatingDraft = false;
		}
	}

	function startEditingField(field) {
		editingField = field;
	}

	function cancelFieldEdit() {
		editingField = null;
		initEditValues();
	}

	async function saveField(field) {
		savingField = field;
		draftError = null;

		try {
			let value = editValues[field];

			// Parse number for funding_goal
			if (field === 'funding_goal') {
				value = value ? parseFloat(value) : null;
			} else if (typeof value === 'string') {
				value = value.trim() || null;
			}

			const updateData = { [field]: value };
			const sessionId = $auth.isAuthenticated ? null : aiChat.getSessionId();
			draft = await updateAIDraft(threadId, updateData, sessionId);
			editingField = null;
			initEditValues();
		} catch (e) {
			draftError = e.message;
		} finally {
			savingField = null;
		}
	}

	function handleFieldKeydown(event, field) {
		if (event.key === 'Enter' && !event.shiftKey && field !== 'description') {
			event.preventDefault();
			saveField(field);
		} else if (event.key === 'Escape') {
			cancelFieldEdit();
		}
	}

	async function handleConvertProject() {
		if (!$auth.isAuthenticated) {
			goto(`/login?redirect=/vibe/${threadId}`);
			return;
		}

		convertingProject = true;
		draftError = null;

		try {
			// Claim the thread first (in case it was created anonymously)
			await claimAIThread(threadId).catch(() => {
				// Already claimed, ignore error
			});

			const project = await convertAIDraft(threadId);
			// Redirect to the new project
			goto(`/projects/${project.slug}`);
		} catch (e) {
			draftError = e.message;
		} finally {
			convertingProject = false;
		}
	}

	function formatTime(date) {
		return new Date(date).toLocaleTimeString('de-DE', {
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	function getProjectTypeColor(type) {
		switch (type) {
			case 'crowdfunding':
				return 'bg-[#06E481]/20 text-[#304b50] dark:text-[#06E481]';
			case 'fundraising':
				return 'bg-[#FF85FF]/20 text-[#FF85FF]';
			case 'private':
				return 'bg-[#FFC21C]/20 text-[#b38600] dark:text-[#FFC21C]';
			default:
				return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
		}
	}

	function getPlanColor(plan) {
		switch (plan) {
			case 'basic':
				return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
			case 'pro':
				return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
			case 'premium':
				return 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400';
			case 'enterprise':
				return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
			default:
				return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
		}
	}
</script>

<svelte:head>
	<title>{$t('vibe.chat.title')} | #startneu</title>
</svelte:head>

<div class="flex h-[calc(100vh-4rem)]">
	<!-- Left: Chat Area -->
	<div class="w-1/2 flex flex-col bg-gray-50 dark:bg-gray-900 min-w-0">
		<!-- Chat Header -->
		<div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 h-16 flex items-center flex-shrink-0">
			<div class="flex items-center gap-3">
				<a href="/vibe" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
					<svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
					</svg>
				</a>
				<div>
					<h1 class="font-semibold text-gray-900 dark:text-white">{$t('vibe.chat.headline')}</h1>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						{messageCount} / {settings.minMessagesForProject} {$t('vibe.chat.messagesNeeded')}
					</p>
				</div>
			</div>
		</div>

		<!-- Messages -->
		<div
			bind:this={messagesContainer}
			class="flex-1 overflow-y-auto px-6 py-6"
		>
			<div class="space-y-4">
				{#each messages as message (message.id)}
					<div class="flex {message.isAssistant ? 'justify-start' : 'justify-end'}">
						<div
							class="max-w-[85%] rounded-2xl px-4 py-3 {message.isAssistant
								? 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
								: 'bg-[#06E481] text-white'}"
						>
							{#if message.htmlContent}
								<div class="prose dark:prose-invert prose-sm max-w-none">
									{@html message.htmlContent}
								</div>
							{:else}
								<p class="whitespace-pre-wrap">{message.content}</p>
							{/if}
							<p class="text-xs mt-2 {message.isAssistant ? 'text-gray-400' : 'text-white/70'}">
								{formatTime(message.createdAt)}
							</p>
						</div>
					</div>
				{/each}

				{#if loading}
					<div class="flex justify-start">
						<div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl px-4 py-3">
							<div class="flex items-center gap-2">
								<div class="w-2 h-2 bg-[#06E481] rounded-full animate-bounce"></div>
								<div class="w-2 h-2 bg-[#06E481] rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
								<div class="w-2 h-2 bg-[#06E481] rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
							</div>
						</div>
					</div>
				{/if}
			</div>
		</div>

		<!-- Login Required Banner -->
		{#if requiresLogin && !$auth.isAuthenticated}
			<div class="bg-amber-50 dark:bg-amber-900/30 border-t border-amber-200 dark:border-amber-800 px-6 py-3 flex-shrink-0">
				<div class="flex items-center justify-between">
					<p class="text-amber-800 dark:text-amber-200 text-sm">
						{$t('vibe.chat.loginRequired')}
					</p>
					<a
						href="/login?redirect=/vibe/{threadId}"
						class="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white text-sm font-medium rounded-lg transition-colors"
					>
						{$t('vibe.chat.loginNow')}
					</a>
				</div>
			</div>
		{/if}

		<!-- Input Area -->
		<div class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-4 flex-shrink-0">
			<form on:submit|preventDefault={handleSubmit}>
				<div class="flex items-start gap-3">
					<div class="flex-1 relative">
						<textarea
							bind:value={prompt}
							on:keydown={handleKeydown}
							placeholder={requiresLogin && !$auth.isAuthenticated ? $t('vibe.chat.loginToContine') : $t('vibe.chat.inputPlaceholder')}
							rows="2"
							disabled={loading || (requiresLogin && !$auth.isAuthenticated)}
							class="w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-[#06E481] focus:border-transparent resize-none dark:bg-gray-700 dark:text-white disabled:opacity-50"
						></textarea>
					</div>
					<button
						type="submit"
						disabled={!prompt.trim() || loading || (requiresLogin && !$auth.isAuthenticated)}
						class="h-[50px] w-[50px] flex items-center justify-center bg-[#06E481] hover:bg-[#05c96e] disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white rounded-xl transition-colors flex-shrink-0"
					>
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
						</svg>
					</button>
				</div>
			</form>
		</div>
	</div>

	<!-- Right: Project Preview Panel -->
	<div class="w-1/2 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col flex-shrink-0 hidden lg:flex">
		<!-- Panel Header -->
		<div class="px-6 h-16 flex items-center justify-between border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
			<h2 class="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
				<svg class="w-5 h-5 text-[#06E481]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
				{$t('vibe.preview.title')}
			</h2>
			<!-- Regenerate Button (only when draft exists) -->
			{#if draft}
				<button
					on:click={handleGenerateDraft}
					disabled={generatingDraft}
					class="flex items-center gap-2 px-3 py-1.5 rounded-full border-2 border-gray-200 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:border-[#06E481] hover:text-[#06E481] hover:bg-[#06E481]/10 disabled:opacity-50 transition-all text-sm"
				>
					{#if generatingDraft}
						<svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
					{:else}
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
						</svg>
					{/if}
					{$t('vibe.preview.refresh')}
				</button>
			{/if}
		</div>

		<div class="flex-1 overflow-y-auto">
			{#if !canCreateProject}
				<!-- Not enough messages yet -->
				<div class="h-full flex flex-col items-center justify-center p-8 text-center">
					<div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mb-4">
						<svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
						</svg>
					</div>
					<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
						{$t('vibe.preview.keepChatting')}
					</h3>
					<p class="text-gray-500 dark:text-gray-400 text-sm mb-4">
						{$t('vibe.preview.needMoreMessages')}
					</p>
					<div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
						<span class="font-semibold text-[#06E481]">{messageCount}</span>
						<span>/</span>
						<span>{settings.minMessagesForProject}</span>
						<span>{$t('vibe.chat.messagesNeeded')}</span>
					</div>
				</div>

			{:else if !draft}
				<!-- Can create project, show generate button -->
				<div class="h-full flex flex-col items-center justify-center p-8 text-center">
					<div class="w-16 h-16 rounded-full bg-[#06E481]/20 flex items-center justify-center mb-4">
						<svg class="w-8 h-8 text-[#06E481]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
						</svg>
					</div>
					<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
						{$t('vibe.preview.readyToGenerate')}
					</h3>
					<p class="text-gray-500 dark:text-gray-400 text-sm mb-6">
						{$t('vibe.preview.generateDescription')}
					</p>

					{#if draftError}
						<div class="mb-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm w-full">
							{translateError(draftError)}
						</div>
					{/if}

					<button
						on:click={handleGenerateDraft}
						disabled={generatingDraft}
						class="px-6 py-3 bg-[#06E481] hover:bg-[#05c96e] disabled:bg-gray-300 text-white font-semibold rounded-xl transition-colors flex items-center gap-2"
					>
						{#if generatingDraft}
							<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							{$t('vibe.preview.generating')}
						{:else}
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
							</svg>
							{$t('vibe.preview.generatePreview')}
						{/if}
					</button>
				</div>

			{:else}
				<!-- Draft exists, show project-page-style preview -->
				<div class="bg-gray-50 dark:bg-gray-900">
					{#if draftError}
						<div class="mx-4 mt-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
							{translateError(draftError)}
						</div>
					{/if}

					<!-- Project Image Placeholder -->
					<div class="w-full h-40 bg-gradient-to-br from-[#304b50] to-[#06E481] flex items-center justify-center">
						<svg class="h-16 w-16 text-white opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
						</svg>
					</div>

					<div class="p-5">
						<!-- Badges Row -->
						<div class="flex flex-wrap items-center gap-2 mb-4">
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<span
								on:click={() => startEditingField('project_type')}
								class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium cursor-pointer hover:ring-2 hover:ring-[#06E481] {getProjectTypeColor(draft.project_type)}"
							>
								{$t(`project.type.${draft.project_type || 'crowdfunding'}`)}
							</span>
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<span
								on:click={() => startEditingField('plan')}
								class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium cursor-pointer hover:ring-2 hover:ring-[#06E481] capitalize {getPlanColor(draft.plan)}"
							>
								{draft.plan || 'basic'}
							</span>
							<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400">
								<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
								</svg>
								{$t('project.aiGenerated')}
							</span>
						</div>

						<!-- Type/Plan Edit Modals -->
						{#if editingField === 'project_type'}
							<div class="mb-4 p-3 bg-white dark:bg-gray-800 rounded-lg border border-[#06E481]">
								<select
									bind:value={editValues.project_type}
									class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
								>
									<option value="crowdfunding">{$t('project.type.crowdfunding')}</option>
									<option value="fundraising">{$t('project.type.fundraising')}</option>
									<option value="private">{$t('project.type.private')}</option>
								</select>
								<div class="mt-2 flex gap-2">
									<button on:click={() => saveField('project_type')} disabled={savingField === 'project_type'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
										{savingField === 'project_type' ? $t('project.saving') : $t('common.save')}
									</button>
									<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
										{$t('common.cancel')}
									</button>
								</div>
							</div>
						{/if}

						{#if editingField === 'plan'}
							<div class="mb-4 p-3 bg-white dark:bg-gray-800 rounded-lg border border-[#06E481]">
								<select
									bind:value={editValues.plan}
									class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
								>
									<option value="basic">Basic (9%)</option>
									<option value="pro">Pro (7%)</option>
									<option value="premium">Premium (5%)</option>
									<option value="enterprise">Enterprise</option>
								</select>
								<div class="mt-2 flex gap-2">
									<button on:click={() => saveField('plan')} disabled={savingField === 'plan'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
										{savingField === 'plan' ? $t('project.saving') : $t('common.save')}
									</button>
									<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
										{$t('common.cancel')}
									</button>
								</div>
							</div>
						{/if}

						<!-- Title -->
						{#if editingField === 'title'}
							<div class="mb-4">
								<input
									type="text"
									bind:value={editValues.title}
									on:keydown={(e) => handleFieldKeydown(e, 'title')}
									class="w-full text-2xl font-bold px-2 py-1 border-2 border-[#06E481] rounded-lg dark:bg-gray-700 dark:text-white"
									autofocus
								/>
								<div class="mt-2 flex gap-2">
									<button on:click={() => saveField('title')} disabled={savingField === 'title'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
										{savingField === 'title' ? $t('project.saving') : $t('common.save')}
									</button>
									<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
										{$t('common.cancel')}
									</button>
								</div>
							</div>
						{:else}
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<h1
								on:click={() => startEditingField('title')}
								class="text-2xl font-bold text-[#304b50] dark:text-white mb-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 -mx-2 px-2 py-1 rounded-lg transition-colors"
							>
								{draft.title || $t('project.notSet')}
							</h1>
						{/if}

						<!-- Funding Goal Box -->
						{#if editingField === 'funding_goal'}
							<div class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-4 border border-[#06E481]">
								<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{$t('project.fundingGoal')} (EUR)</label>
								<input
									type="number"
									bind:value={editValues.funding_goal}
									on:keydown={(e) => handleFieldKeydown(e, 'funding_goal')}
									min="0"
									step="100"
									class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
								/>
								<div class="mt-2 flex gap-2">
									<button on:click={() => saveField('funding_goal')} disabled={savingField === 'funding_goal'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
										{savingField === 'funding_goal' ? $t('project.saving') : $t('common.save')}
									</button>
									<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
										{$t('common.cancel')}
									</button>
								</div>
							</div>
						{:else}
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<div
								on:click={() => startEditingField('funding_goal')}
								class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-4 cursor-pointer hover:ring-2 hover:ring-[#06E481] transition-all"
							>
								<div class="flex justify-between items-end mb-2">
									<div>
										<div class="text-2xl font-bold text-[#304b50] dark:text-white">0 EUR</div>
										<div class="text-sm text-gray-600 dark:text-gray-400">
											{$t('project.goal')}: {draft.funding_goal ? `${Number(draft.funding_goal).toLocaleString('de-DE')} EUR` : $t('project.notSet')}
										</div>
									</div>
									<div class="text-right">
										<div class="text-2xl font-bold text-[#304b50] dark:text-[#06E481]">0%</div>
										<div class="text-sm text-gray-600 dark:text-gray-400">{$t('project.funded')}</div>
									</div>
								</div>
								<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-3">
									<div class="bg-[#06E481] h-3 rounded-full" style="width: 0%"></div>
								</div>
							</div>
						{/if}

						<!-- Short Description -->
						{#if editingField === 'short_description'}
							<div class="mb-4">
								<textarea
									bind:value={editValues.short_description}
									rows="3"
									maxlength="500"
									class="w-full px-3 py-2 border-2 border-[#06E481] rounded-lg dark:bg-gray-700 dark:text-white resize-none"
								></textarea>
								<div class="flex justify-between items-center mt-1">
									<div class="flex gap-2">
										<button on:click={() => saveField('short_description')} disabled={savingField === 'short_description'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
											{savingField === 'short_description' ? $t('project.saving') : $t('common.save')}
										</button>
										<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
											{$t('common.cancel')}
										</button>
									</div>
									<span class="text-xs text-gray-400">{editValues.short_description?.length || 0}/500</span>
								</div>
							</div>
						{:else}
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<p
								on:click={() => startEditingField('short_description')}
								class="text-gray-700 dark:text-gray-300 mb-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 -mx-2 px-2 py-1 rounded-lg transition-colors"
							>
								{draft.short_description || $t('project.notSet')}
							</p>
						{/if}

						<!-- Description -->
						<div class="border-t border-gray-200 dark:border-gray-700 pt-4">
							<h2 class="text-lg font-semibold text-[#304b50] dark:text-white mb-2">{$t('project.description')}</h2>
							{#if editingField === 'description'}
								<div>
									<textarea
										bind:value={editValues.description}
										rows="6"
										class="w-full px-3 py-2 border-2 border-[#06E481] rounded-lg dark:bg-gray-700 dark:text-white resize-none"
									></textarea>
									<div class="mt-2 flex gap-2">
										<button on:click={() => saveField('description')} disabled={savingField === 'description'} class="px-3 py-1 text-sm bg-[#06E481] text-white font-medium rounded-lg hover:bg-[#05c96e] disabled:opacity-50">
											{savingField === 'description' ? $t('project.saving') : $t('common.save')}
										</button>
										<button on:click={cancelFieldEdit} class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg">
											{$t('common.cancel')}
										</button>
									</div>
								</div>
							{:else}
								<!-- svelte-ignore a11y_click_events_have_key_events -->
								<!-- svelte-ignore a11y_no_static_element_interactions -->
								<div
									on:click={() => startEditingField('description')}
									class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 -mx-2 px-2 py-1 rounded-lg transition-colors text-sm"
								>
									{draft.description || $t('project.notSet')}
								</div>
							{/if}
						</div>

					</div>
				</div>
			{/if}
		</div>

		<!-- Publish Button (sticky footer when draft exists) - aligned with chat input -->
		{#if draft}
			<div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex-shrink-0">
				<button
					on:click={handleConvertProject}
					disabled={convertingProject || !draft.title}
					class="w-full px-4 py-3 bg-[#06E481] hover:bg-[#05c96e] disabled:bg-gray-300 dark:disabled:bg-gray-600 text-[#304b50] font-semibold rounded-xl transition-colors flex items-center justify-center gap-2"
				>
					{#if convertingProject}
						<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
					{:else}
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					{/if}
					{$t('vibe.preview.publishProject')}
				</button>
				<p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
					{$t('vibe.draft.canEditLater')}
				</p>
			</div>
		{/if}
	</div>
</div>
