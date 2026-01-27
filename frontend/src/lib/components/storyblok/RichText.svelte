<script>
	import { storyblokEditable, renderRichText } from '@storyblok/svelte';

	export let blok;

	$: renderedContent = blok.content ? renderRichText(blok.content) : '';
</script>

<div use:storyblokEditable={blok} class="richtext-wrapper py-8 px-4">
	<div class="max-w-4xl mx-auto prose prose-lg">
		{@html renderedContent}
	</div>
</div>

<style>
	.richtext-wrapper :global(h1),
	.richtext-wrapper :global(h2),
	.richtext-wrapper :global(h3),
	.richtext-wrapper :global(h4),
	.richtext-wrapper :global(h5),
	.richtext-wrapper :global(h6) {
		color: #111827;
	}

	:global(.dark) .richtext-wrapper :global(h1),
	:global(.dark) .richtext-wrapper :global(h2),
	:global(.dark) .richtext-wrapper :global(h3),
	:global(.dark) .richtext-wrapper :global(h4),
	:global(.dark) .richtext-wrapper :global(h5),
	:global(.dark) .richtext-wrapper :global(h6) {
		color: #ffffff;
	}

	.richtext-wrapper :global(p),
	.richtext-wrapper :global(li),
	.richtext-wrapper :global(span) {
		color: #374151;
	}

	:global(.dark) .richtext-wrapper :global(p),
	:global(.dark) .richtext-wrapper :global(li),
	:global(.dark) .richtext-wrapper :global(span) {
		color: #d1d5db;
	}

	.richtext-wrapper :global(strong),
	.richtext-wrapper :global(b) {
		color: #111827;
	}

	:global(.dark) .richtext-wrapper :global(strong),
	:global(.dark) .richtext-wrapper :global(b) {
		color: #ffffff;
	}

	.richtext-wrapper :global(a) {
		color: #06E481;
		text-decoration: none;
	}

	.richtext-wrapper :global(a:hover) {
		text-decoration: underline;
	}
</style>
