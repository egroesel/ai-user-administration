<script>
	import { storyblokEditable, StoryblokComponent } from '@storyblok/svelte';

	export let blok;
</script>

<div use:storyblokEditable={blok} class="page">
	{#if blok.body}
		{#each blok.body as item}
			<StoryblokComponent blok={item} />
		{/each}
	{/if}
</div>
