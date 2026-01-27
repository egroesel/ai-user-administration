import { useStoryblokApi } from '@storyblok/svelte';

export async function load({ params, url }) {
	const storyblokApi = useStoryblokApi();
	// params.slug is a string like "impressum" or "about/team"
	const slug = params.slug || 'home';

	// Check if we're in the Storyblok Visual Editor
	const version = url.searchParams.get('_storyblok') ? 'draft' : 'published';

	try {
		const response = await storyblokApi.get(`cdn/stories/${slug}`, {
			version
		});

		return {
			story: response.data.story
		};
	} catch (error) {
		// If page not found, return null
		if (error.status === 404) {
			return {
				story: null,
				error: 'Page not found'
			};
		}
		throw error;
	}
}
