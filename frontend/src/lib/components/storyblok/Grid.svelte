<script>
	import { storyblokEditable, StoryblokComponent } from '@storyblok/svelte';

	export let blok;

	// Map column count to grid classes
	const columnsClass = {
		2: 'md:grid-cols-2',
		3: 'md:grid-cols-3',
		4: 'md:grid-cols-4'
	};
</script>

<div use:storyblokEditable={blok} class="py-12 px-4">
	<div class="max-w-7xl mx-auto">
		{#if blok.headline}
			<h2 class="text-3xl font-bold text-gray-900 dark:text-white text-center mb-8">
				{blok.headline}
			</h2>
		{/if}
		<div class="grid grid-cols-1 {columnsClass[blok.columns] || 'md:grid-cols-3'} gap-6">
			{#if blok.columns_content}
				{#each blok.columns_content as item}
					<StoryblokComponent blok={item} />
				{/each}
			{/if}
		</div>
	</div>
</div>
