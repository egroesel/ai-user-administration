<script>
	import { createEventDispatcher } from 'svelte';
	import '$lib/styles/cf-type-selection.scss';

	export let type = 'crowdfunding'; // crowdfunding, fundraising, private
	export let title = '';
	export let subtitle = '';
	export let description = '';
	export let isSelected = false;

	const dispatch = createEventDispatcher();

	function handleClick() {
		dispatch('select', { type });
	}
</script>

<button
	type="button"
	on:click={handleClick}
	class="cf-type-selection cf-type-selection--{type}"
	class:cf-type-selection--selected={isSelected}
>
	<!-- Header / Title -->
	<div class="cf-type-selection__title">
		<span class="sn-text-large">{title}</span>

		<!-- Checkmark (only when selected) -->
		{#if isSelected}
			<svg class="cf-type-selection__card-tick cf-type-selection__card-tick--{type}" width="24" height="24" viewBox="0 0 24 24" fill="none">
				<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
			</svg>
		{/if}
	</div>

	<!-- Body -->
	<div class="cf-type-selection__body">
		<h3 class="cf-type-selection__subtitle">{subtitle}</h3>
		<p class="cf-type-selection__desc" class:visible={isSelected}>
			{description}
		</p>
	</div>
</button>

<style>
	/* Typography helpers */
	.sn-text-large {
		font-size: 1.125rem;
		font-weight: 600;
		color: #304b50;
	}

	:global(.dark) .sn-text-large {
		color: #f9fafb;
	}

	.cf-type-selection--selected .sn-text-large {
		color: #1f2937;
	}

	/* Checkmark colors per type */
	.cf-type-selection__card-tick--crowdfunding {
		color: #06E481;
	}

	.cf-type-selection__card-tick--fundraising {
		color: #FF85FF;
	}

	.cf-type-selection__card-tick--private {
		color: #FFC21C;
	}

	/* Show description responsively */
	.cf-type-selection__desc {
		display: none;
	}

	.cf-type-selection__desc.visible {
		display: flex;
	}

	@media (min-width: 640px) {
		.cf-type-selection__desc {
			display: flex;
		}
	}
</style>
