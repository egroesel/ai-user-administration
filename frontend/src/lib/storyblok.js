import { apiPlugin, storyblokInit, useStoryblokApi } from '@storyblok/svelte';

// Import Storyblok components
import Page from '$lib/components/storyblok/Page.svelte';
import Teaser from '$lib/components/storyblok/Teaser.svelte';
import Feature from '$lib/components/storyblok/Feature.svelte';
import Grid from '$lib/components/storyblok/Grid.svelte';
import RichText from '$lib/components/storyblok/RichText.svelte';

// Storyblok configuration
export function initStoryblok() {
	storyblokInit({
		accessToken: 'jdkrTcYMYeJpgcA9n7oR5Att',
		use: [apiPlugin],
		apiOptions: {
			region: 'eu'
		},
		components: {
			page: Page,
			teaser: Teaser,
			feature: Feature,
			grid: Grid,
			richtext: RichText
		}
	});
}

// Get the Storyblok API instance
export function getStoryblokApi() {
	return useStoryblokApi();
}
