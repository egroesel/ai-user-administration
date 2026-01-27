<script>
	import { storyblokEditable } from '@storyblok/svelte';

	export let blok;
</script>

<div use:storyblokEditable={blok} class="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
	{#if blok.icon}
		<div class="w-12 h-12 bg-[#06E481]/20 rounded-full flex items-center justify-center mb-4">
			<span class="text-2xl">{blok.icon}</span>
		</div>
	{/if}
	{#if blok.name}
		<h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
			{blok.name}
		</h3>
	{/if}
	{#if blok.description}
		<p class="text-gray-600 dark:text-gray-300">
			{blok.description}
		</p>
	{/if}
	{#if blok.link?.cached_url}
		<a
			href={blok.link.cached_url}
			class="inline-flex items-center mt-4 text-[#06E481] hover:underline font-medium"
		>
			{blok.link_text || 'Mehr erfahren'}
			<svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</a>
	{/if}
</div>
