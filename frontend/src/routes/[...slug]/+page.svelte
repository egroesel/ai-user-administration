<script>
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { useStoryblokBridge, StoryblokComponent } from '@storyblok/svelte';
	import { t } from '$lib/stores/language';

	export let data;

	// Reactively update story when data changes (client-side navigation)
	$: story = data.story;

	// Setup Storyblok bridge for Visual Editor
	function setupBridge() {
		if (story && story.id) {
			useStoryblokBridge(story.id, (newStory) => {
				story = newStory;
			});
		}
	}

	onMount(() => {
		setupBridge();
	});

	afterNavigate(() => {
		setupBridge();
	});
</script>

<svelte:head>
	{#if story}
		<title>{story.name} | #startneu</title>
	{:else}
		<title>{$t('error.pageNotFound')} | #startneu</title>
	{/if}
</svelte:head>

<div>
	{#if story}
		<StoryblokComponent blok={story.content} />
	{:else}
		<div class="max-w-4xl mx-auto px-4 py-16 text-center">
			<h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
				{$t('error.pageNotFound')}
			</h1>
			<p class="text-gray-600 dark:text-gray-400 mb-8">
				{$t('error.pageNotFoundDescription')}
			</p>
			<a
				href="/"
				class="inline-flex items-center px-6 py-3 bg-[#06E481] text-white font-semibold rounded-lg hover:bg-[#05c96e] transition-colors"
			>
				{$t('error.backHome')}
			</a>
		</div>
	{/if}
</div>
