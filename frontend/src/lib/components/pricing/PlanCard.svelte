<script>
	import { createEventDispatcher } from 'svelte';
	import '$lib/styles/cf-plan-selection.scss';
	import '$lib/styles/ticket.scss';
	import '$lib/styles/plan-card.scss';

	export let plan = {}; // { key, isAvailable, isOnDemand, provision, discountedProvision, scope }
	export let content = {}; // { name, subtitle, shortDescription, features, cta, ... }
	export let selectedType = 'crowdfunding';
	export let isSelected = false;
	export let isDisabled = false;
	export let showDiscount = false;
	export let discountPercent = 0;
	export let variant = 'full'; // 'full', 'compact', or 'summary'

	const dispatch = createEventDispatcher();

	let showAllFeatures = false;

	$: visibleFeatures =
		variant === 'compact' && !showAllFeatures
			? (content.features || []).slice(0, 5)
			: content.features || [];
	$: hasMoreFeatures = variant === 'compact' && (content.features || []).length > 5;

	function handleSelect() {
		if (!isDisabled && !plan.isOnDemand) {
			dispatch('select', { plan: plan.key });
		}
	}

	function toggleFeatures() {
		showAllFeatures = !showAllFeatures;
	}

	function formatProvision(value) {
		if (value === null || value === undefined) return '-';
		return value.toFixed(2).replace('.', ',');
	}
</script>

{#if variant === 'summary'}
	<!-- Summary Variant - with item wrapper like Vue template -->
	<div class="cf-plan-selection__item cf-plan-selection__item--{selectedType} p-3 h-full mt-0">
		<!-- Plan Name -->
		<h3 class="sn-text-xxlarge mb-2">{content.name || plan.key}</h3>

		<!-- Summary Features (using futureFeatures with tick icons) -->
		{#if content.futureFeatures && content.futureFeatures.length > 0}
			<div class="pb-2">
				{#each content.futureFeatures as feature}
					<div class="feature-item mb-1">
						<svg class="cf-plan-selection__list-icon icon--{selectedType} mr-2" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
						<span>{feature}</span>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Pricing Ticket (no bottom margin in summary, no CTA) -->
		<div class="cf-plan-selection__disable-fully">
			<div class="ticket">
				{#if plan.isOnDemand}
					<div class="w-full text-center sn-text-xxxlarge sn-text-semibold ticket__item ticket__item--text-field py-2">
						Auf Anfrage
					</div>
				{:else}
					<div class="ticket__item">
						<div class="ticket__item-value">0,00 €</div>
						<small class="ticket__item-label">Laufende Kosten</small>
					</div>
					<div class="ticket__item ticket__item--right">
						<div class="ticket__item-value">
							{#if showDiscount && plan.discountedProvision !== plan.provision}
								<span class="provision-strikethrough">{formatProvision(plan.provision)} %</span>
								<span class="provision-discounted">{formatProvision(plan.discountedProvision)} %</span>
							{:else}
								{formatProvision(plan.provision)} %
							{/if}
						</div>
						<small class="ticket__item-label">Provision</small>
					</div>
				{/if}
			</div>
		</div>
	</div>
{:else}
	<!-- Full/Compact Variant -->
	<div
		class="cf-plan-selection__item cf-plan-selection__item--{selectedType}"
		class:cf-plan-selection__item--selected={isSelected && !isDisabled}
		class:cf-plan-selection__item--disabled={isDisabled}
		on:click={handleSelect}
		on:keydown={(e) => e.key === 'Enter' && handleSelect()}
		role="button"
		tabindex={isDisabled ? -1 : 0}
		aria-disabled={isDisabled}
	>
		<!-- Top Label (Discount or Recommended) -->
		{#if showDiscount && discountPercent > 0 && !isDisabled}
			<div class="cf-plan-selection__top-label cf-plan-selection__top-label--dim">
				<span>Rabatt angewendet</span>
				<span class="ml-auto">-{discountPercent} %</span>
			</div>
		{:else if isSelected && !isDisabled}
			<div class="cf-plan-selection__top-label">
				Empfohlen
			</div>
		{/if}

		<div class="cf-plan-selection__disable-fully">
			<!-- Plan Name -->
			<h3 class="sn-text-xxlarge">{content.name || plan.key}</h3>

			<!-- Subtitle -->
			{#if content.subtitle}
				<div class="sn-text-xlarge mb-2">{content.subtitle}</div>
			{/if}

			<!-- Short Description -->
			{#if content.shortDescription && variant !== 'compact'}
				<div class="cf-plan-selection__desc">{content.shortDescription}</div>
			{/if}

			<!-- Pricing Ticket -->
			<div class="ticket mb-2">
				{#if plan.isOnDemand}
					<div class="w-full text-center sn-text-xxxlarge sn-text-semibold ticket__item ticket__item--text-field py-2">
						Auf Anfrage
					</div>
				{:else}
					<div class="ticket__item">
						<div class="ticket__item-value">0,00 €</div>
						<small class="ticket__item-label">Laufende Kosten</small>
					</div>
					<div class="ticket__item ticket__item--right">
						<div class="ticket__item-value">
							{#if showDiscount && plan.discountedProvision !== plan.provision}
								<span class="provision-strikethrough">{formatProvision(plan.provision)} %</span>
								<span class="provision-discounted">{formatProvision(plan.discountedProvision)} %</span>
							{:else}
								{formatProvision(plan.provision)} %
							{/if}
						</div>
						<small class="ticket__item-label">Provision</small>
					</div>
				{/if}
			</div>

			<!-- CTA Button -->
			{#if plan.isOnDemand}
				<a
					href="mailto:business@example.com?subject=Enterprise Plan Anfrage"
					class="cta-btn cta-btn--outline cta-btn--{selectedType}"
					on:click|stopPropagation
				>
					{content.cta || 'Kontakt aufnehmen'}
				</a>
			{:else if !isDisabled}
				<button
					type="button"
					on:click|stopPropagation={() => dispatch('continue', { plan: plan.key })}
					class="cta-btn cta-btn--{selectedType}"
					class:cta-btn--filled={isSelected}
					class:cta-btn--outline={!isSelected}
				>
					{content.cta || 'Plan wählen'}
				</button>
			{:else}
				<div class="cta-btn cta-btn--disabled">
					Nicht verfügbar
				</div>
			{/if}
		</div>

		<!-- Feature Headline -->
		{#if content.features && content.features.length > 0 && plan.key !== 'basic'}
			<div class="mt-4 mb-2 sn-text-semibold">Funktionen</div>
		{/if}

		<!-- Feature List -->
		{#if visibleFeatures.length > 0}
			<div class="{plan.key === 'basic' ? 'mt-4' : ''}">
				{#each visibleFeatures as feature}
					<div class="feature-item">
						{#if plan.key !== 'basic'}
							<svg class="cf-plan-selection__list-icon icon--{selectedType}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
							</svg>
						{/if}
						<span>{feature}</span>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Future Features (well) -->
		{#if content.futureFeatures && content.futureFeatures.length > 0 && (variant === 'full' || showAllFeatures)}
			<div class="cf-plan-selection__well pb-2 pt-3 px-3 my-4">
				<div class="sn-text-semibold mb-2">Demnächst verfügbar</div>
				{#each content.futureFeatures as feature}
					<div class="feature-item">
						{#if plan.key !== 'basic'}
							<svg class="cf-plan-selection__list-icon icon--{selectedType}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
							</svg>
						{/if}
						<span>{feature}</span>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Payment Methods -->
		{#if content.paymentMethods && content.paymentMethods.length > 0 && (variant === 'full' || showAllFeatures)}
			<div class="mt-4 mb-3">
				<div class="sn-text-semibold mb-2">Zahlungsarten</div>
				{#each content.paymentMethods as method}
					<div class="feature-item">
						{#if plan.key !== 'basic'}
							<svg class="cf-plan-selection__list-icon icon--{selectedType}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
							</svg>
						{/if}
						<span>{method}</span>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Support -->
		{#if content.support && (variant === 'full' || showAllFeatures)}
			<div class="cf-plan-selection__list-end pt-4 mt-auto">
				<div class="sn-text-semibold mb-2">Support</div>
				<div class="text-sm text-gray-600 dark:text-gray-400">{content.support}</div>
			</div>
		{/if}

		<!-- Show More (compact mode) -->
		{#if variant === 'compact' && !showAllFeatures && hasMoreFeatures}
			<div
				class="text-center mt-auto pt-4 sn-text-semibold cursor-pointer"
				on:click|stopPropagation={toggleFeatures}
				on:keydown|stopPropagation={(e) => e.key === 'Enter' && toggleFeatures()}
				role="button"
				tabindex="0"
			>
				Mehr anzeigen
				<svg class="inline-block w-4 h-4 ml-2 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
				</svg>
			</div>
		{/if}
	</div>
{/if}
