<script>
	import { goto } from '$app/navigation';
	import { aiChat } from '$lib/stores/aiChat';
	import { t } from '$lib/stores/language';
	import { onMount } from 'svelte';

	let prompt = '';
	let loading = false;
	let error = null;

	onMount(() => {
		aiChat.loadSettings();
	});

	// Translate backend error messages
	function translateError(errorMessage) {
		const errorMap = {
			'Message limit reached. Please log in to continue.': 'vibe.error.messageLimitReached',
			'AI Coach is not configured. Please set OPENAI_API_KEY.': 'vibe.error.aiNotConfigured'
		};

		const translationKey = errorMap[errorMessage];
		return translationKey ? $t(translationKey) : errorMessage;
	}

	async function handleSubmit() {
		if (!prompt.trim() || loading) return;

		loading = true;
		error = null;

		try {
			// Reset any existing chat
			aiChat.reset();

			// Send first message
			const response = await aiChat.sendMessage(prompt.trim());

			// Navigate to chat page with thread ID
			goto(`/vibe/${response.thread_id}`);
		} catch (e) {
			error = e.message;
			loading = false;
		}
	}

	function handleKeydown(e) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	}

	const suggestions = [
		'Ich möchte ein nachhaltiges Cafe in meiner Stadt eröffnen',
		'Wir entwickeln eine App für lokale Foodsharing-Initiativen',
		'Ich schreibe ein Kinderbuch über Umweltschutz',
		'Unser Verein braucht neue Sportgeräte für die Jugendarbeit'
	];

	function useSuggestion(suggestion) {
		prompt = suggestion;
	}
</script>

<svelte:head>
	<title>{$t('vibe.title')} | #startneu</title>
</svelte:head>

<div class="min-h-[calc(100vh-4rem)] bg-gradient-to-b from-[#304b50] to-[#1a2a2e]">
	<!-- Hero Section -->
	<div class="max-w-4xl mx-auto px-4 pt-16 pb-8 text-center">
		<div class="inline-flex items-center gap-2 bg-[#06E481]/20 text-[#06E481] px-4 py-2 rounded-full text-sm font-medium mb-6">
			<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
			</svg>
			{$t('vibe.badge')}
		</div>

		<h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
			{$t('vibe.headline')}
		</h1>

		<p class="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
			{$t('vibe.subheadline')}
		</p>
	</div>

	<!-- Chat Input Section -->
	<div class="max-w-3xl mx-auto px-4 pb-16">
		<div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-6">
			<form on:submit|preventDefault={handleSubmit}>
				<div class="relative">
					<textarea
						bind:value={prompt}
						on:keydown={handleKeydown}
						placeholder={$t('vibe.placeholder')}
						rows="4"
						disabled={loading}
						class="w-full px-4 py-3 text-lg border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-[#06E481] focus:border-transparent resize-none dark:bg-gray-700 dark:text-white disabled:opacity-50"
					></textarea>
				</div>

				{#if error}
					<div class="mt-3 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
						{translateError(error)}
					</div>
				{/if}

				<div class="mt-4 flex items-center justify-between">
					<p class="text-sm text-gray-500 dark:text-gray-400">
						{$t('vibe.hint')}
					</p>

					<button
						type="submit"
						disabled={!prompt.trim() || loading}
						class="px-6 py-3 bg-[#06E481] hover:bg-[#05c96e] disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-semibold rounded-xl transition-colors flex items-center gap-2"
					>
						{#if loading}
							<svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							{$t('vibe.loading')}
						{:else}
							{$t('vibe.start')}
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
							</svg>
						{/if}
					</button>
				</div>
			</form>

			<!-- Suggestions -->
			<div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
				<p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-3">
					{$t('vibe.suggestions')}
				</p>
				<div class="flex flex-wrap gap-2">
					{#each suggestions as suggestion}
						<button
							on:click={() => useSuggestion(suggestion)}
							class="px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-[#06E481]/20 hover:text-[#06E481] text-gray-700 dark:text-gray-300 text-sm rounded-lg transition-colors text-left"
						>
							{suggestion}
						</button>
					{/each}
				</div>
			</div>
		</div>

		<!-- How it works -->
		<div class="mt-12 grid md:grid-cols-3 gap-6">
			<div class="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
				<div class="w-12 h-12 bg-[#06E481]/20 rounded-full flex items-center justify-center mx-auto mb-4">
					<span class="text-2xl">1</span>
				</div>
				<h3 class="text-white font-semibold mb-2">{$t('vibe.step1.title')}</h3>
				<p class="text-gray-400 text-sm">{$t('vibe.step1.description')}</p>
			</div>

			<div class="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
				<div class="w-12 h-12 bg-[#06E481]/20 rounded-full flex items-center justify-center mx-auto mb-4">
					<span class="text-2xl">2</span>
				</div>
				<h3 class="text-white font-semibold mb-2">{$t('vibe.step2.title')}</h3>
				<p class="text-gray-400 text-sm">{$t('vibe.step2.description')}</p>
			</div>

			<div class="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
				<div class="w-12 h-12 bg-[#06E481]/20 rounded-full flex items-center justify-center mx-auto mb-4">
					<span class="text-2xl">3</span>
				</div>
				<h3 class="text-white font-semibold mb-2">{$t('vibe.step3.title')}</h3>
				<p class="text-gray-400 text-sm">{$t('vibe.step3.description')}</p>
			</div>
		</div>
	</div>
</div>
