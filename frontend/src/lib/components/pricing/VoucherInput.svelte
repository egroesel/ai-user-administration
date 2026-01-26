<script>
	import { createEventDispatcher } from 'svelte';
	import '$lib/styles/cf-plan-selection.scss';

	export let selectedType = 'crowdfunding';
	export let voucher = { code: '', discount: 0, isValid: false, forPlans: [] };
	export let isBox = false; // Compact box style vs full width

	const dispatch = createEventDispatcher();

	let code = voucher.code || '';
	let isLoading = false;
	let error = '';

	$: isValid = voucher.isValid && voucher.discount > 0;

	// Validate voucher code format
	function validateCodeFormat(codeValue) {
		if (!codeValue) return { valid: false, error: '' };

		const firstChar = codeValue[0]?.toUpperCase();
		const validChars = ['S', 'C', 'F', 'P']; // S = all, C = crowdfunding, F = fundraising, P = private

		if (!validChars.includes(firstChar)) {
			return { valid: false, error: 'Ungültiger Gutscheincode' };
		}

		// Check if code matches selected type
		const typeFirstChar = selectedType[0]?.toUpperCase();
		if (firstChar !== 'S' && firstChar !== typeFirstChar) {
			return { valid: false, error: 'Dieser Gutschein gilt nicht für diesen Projekttyp' };
		}

		return { valid: true, error: '' };
	}

	async function handleSubmit() {
		if (!code.trim()) {
			error = 'Bitte gib einen Gutscheincode ein';
			return;
		}

		const validation = validateCodeFormat(code);
		if (!validation.valid) {
			error = validation.error;
			return;
		}

		isLoading = true;
		error = '';

		// Simulate API call - in production this would call the backend
		await new Promise((resolve) => setTimeout(resolve, 500));

		// Demo: Accept codes starting with S or matching the type
		const firstChar = code[0]?.toUpperCase();
		const isValidCode = firstChar === 'S' || firstChar === selectedType[0]?.toUpperCase();

		if (isValidCode && code.length >= 6) {
			// Simulate a valid voucher response
			const simulatedVoucher = {
				code: code.toUpperCase(),
				discount: 10, // 10% discount
				isValid: true,
				forPlans: ['basic', 'pro', 'premium'] // Valid for all plans except enterprise
			};
			dispatch('apply', simulatedVoucher);
		} else {
			error = 'Ungültiger Gutscheincode';
		}

		isLoading = false;
	}

	function handleReset() {
		code = '';
		error = '';
		dispatch('reset');
	}

	function handleKeyup(event) {
		error = '';
		if (event.key === 'Enter') {
			handleSubmit();
		}
	}
</script>

<div class="cf-plan-selection__voucher" class:cf-plan-selection__voucher--box={isBox}>
	<div class="voucher-row" class:voucher-row--box={isBox}>
		<!-- Title / Icon -->
		<div class="voucher-header">
			{#if isValid && !isBox}
				<div class="cf-plan-selection__voucher-icon cf-plan-selection__voucher-icon--{selectedType}">
					<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"
						/>
					</svg>
				</div>
			{/if}
			<h4 id="voucher-title" class="cf-plan-selection__voucher-title">
				<label for="voucher">
					{#if isValid}
						Gutschein angewendet: -{voucher.discount}%
					{:else}
						Hast du einen Gutschein?
					{/if}
				</label>
			</h4>
		</div>

		<!-- Input + Button -->
		<div class="voucher-input-wrapper">
			<div class="voucher-input-container">
				<input
					id="voucher"
					type="text"
					bind:value={code}
					on:keyup={handleKeyup}
					disabled={isValid}
					placeholder="Gutscheincode eingeben"
					class="cf-plan-selection__voucher-input"
				/>

				<!-- Loading / Clear button -->
				{#if isLoading}
					<button class="cf-plan-selection__voucher-input-icon">
						<svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
						</svg>
					</button>
				{:else if isValid}
					<button
						type="button"
						on:click={handleReset}
						class="cf-plan-selection__voucher-input-icon"
					>
						&times;
					</button>
				{/if}
			</div>

			<!-- Submit button -->
			{#if !isValid}
				<button
					type="button"
					on:click={handleSubmit}
					disabled={isLoading || !code.trim()}
					class="btn cf-plan-select__voucher-btn cf-plan-select__voucher-btn--{selectedType}"
				>
					<span class="btn-text">Einlösen</span>
					<svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
				</button>
			{/if}
		</div>
	</div>

	<!-- Error message -->
	{#if error}
		<p class="voucher-error">{error}</p>
	{/if}

	<!-- Valid voucher notice (box mode) -->
	{#if isBox && isValid}
		<p class="voucher-notice">
			Der Gutschein wird bei Projektstart automatisch angewendet.
		</p>
	{/if}
</div>

<style>
	/* Voucher icon colors */
	.cf-plan-selection__voucher-icon--crowdfunding {
		background-color: #06E481;
	}

	.cf-plan-selection__voucher-icon--fundraising {
		background-color: #FF85FF;
	}

	.cf-plan-selection__voucher-icon--private {
		background-color: #FFC21C;
	}

	/* Layout */
	.voucher-row {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	@media (min-width: 640px) {
		.voucher-row:not(.voucher-row--box) {
			flex-direction: row;
			align-items: center;
		}
	}

	.voucher-row--box {
		flex-direction: column;
	}

	.voucher-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		flex: 1;
	}

	.voucher-row--box .voucher-header {
		margin-bottom: 0.75rem;
	}

	.voucher-input-wrapper {
		display: flex;
	}

	@media (min-width: 640px) {
		.voucher-row:not(.voucher-row--box) .voucher-input-wrapper {
			width: 20rem;
		}
	}

	.voucher-input-container {
		position: relative;
		flex: 1;
	}

	/* Input styling */
	.cf-plan-selection__voucher-input {
		border: 2px solid #e5e7eb;
		border-right: none;
		border-radius: 0.75rem 0 0 0.75rem;
	}

	.cf-plan-selection__voucher-input:disabled {
		background-color: #f3f4f6;
		cursor: not-allowed;
	}

	:global(.dark) .cf-plan-selection__voucher-input {
		background-color: #374151;
		border-color: #4b5563;
		color: #f9fafb;
	}

	:global(.dark) .cf-plan-selection__voucher-input:disabled {
		background-color: #1f2937;
	}

	/* Button styling */
	.cf-plan-select__voucher-btn {
		border-radius: 0 0.75rem 0.75rem 0;
		font-weight: 600;
		color: #1f2937;
	}

	.cf-plan-select__voucher-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.cf-plan-select__voucher-btn--crowdfunding {
		background-color: #06E481;
		border-color: #06E481;
	}

	.cf-plan-select__voucher-btn--crowdfunding:hover:not(:disabled) {
		background-color: #05b667;
	}

	.cf-plan-select__voucher-btn--fundraising {
		background-color: #FF85FF;
		border-color: #FF85FF;
	}

	.cf-plan-select__voucher-btn--fundraising:hover:not(:disabled) {
		background-color: #e070e0;
	}

	.cf-plan-select__voucher-btn--private {
		background-color: #FFC21C;
		border-color: #FFC21C;
	}

	.cf-plan-select__voucher-btn--private:hover:not(:disabled) {
		background-color: #e0aa00;
	}

	.btn-text {
		display: none;
	}

	.btn-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	@media (min-width: 640px) {
		.btn-text {
			display: inline;
		}

		.btn-icon {
			display: none;
		}
	}

	/* Error and notice */
	.voucher-error {
		margin-top: 0.5rem;
		font-size: 0.875rem;
		font-weight: 600;
		color: #ef4444;
	}

	.voucher-notice {
		margin-top: 0.5rem;
		font-size: 0.875rem;
		color: #6b7280;
	}

	:global(.dark) .voucher-notice {
		color: #9ca3af;
	}

	/* Box variant background colors */
	:global(.cf-plan-selection--crowdfunding) .cf-plan-selection__voucher--box {
		background-color: rgba(6, 228, 129, 0.2);
	}

	:global(.cf-plan-selection--fundraising) .cf-plan-selection__voucher--box {
		background-color: rgba(255, 133, 255, 0.2);
	}

	:global(.cf-plan-selection--private) .cf-plan-selection__voucher--box {
		background-color: rgba(255, 194, 28, 0.2);
	}
</style>
