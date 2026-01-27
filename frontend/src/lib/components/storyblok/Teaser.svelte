<script>
	import { storyblokEditable } from '@storyblok/svelte';

	export let blok;
</script>

<div use:storyblokEditable={blok} class="py-16 px-4">
	<div class="max-w-4xl mx-auto text-center">
		{#if blok.headline}
			<h1 class="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
				{blok.headline}
			</h1>
		{/if}
		{#if blok.subheadline}
			<p class="text-xl text-gray-600 dark:text-gray-300 mb-8">
				{blok.subheadline}
			</p>
		{/if}
		{#if blok.image?.filename}
			<img
				src="{blok.image.filename}/m/1200x0"
				alt={blok.image.alt || blok.headline}
				class="w-full rounded-xl shadow-lg"
			/>
		{/if}
	</div>
</div>
