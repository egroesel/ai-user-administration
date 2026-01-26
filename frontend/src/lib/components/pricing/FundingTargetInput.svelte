<script>
	import { createEventDispatcher } from 'svelte';
	import '$lib/styles/funding-target.scss';

	export let value = 0;
	export let selectedType = 'crowdfunding';

	const dispatch = createEventDispatcher();
	const MAX_VALUE = 99999999;

	let isEditing = false;
	let inputValue = '';
	let inputEl;

	$: displayValue = isEditing && inputValue !== '' ? inputValue : formatNumber(value);
	$: bgValue = '00.000.000';

	function formatNumber(num) {
		return num.toLocaleString('de-DE', { maximumFractionDigits: 0 });
	}

	function handleInput(event) {
		isEditing = true;
		const text = event.target.textContent || '';
		const digitsOnly = text.replace(/\D/g, '');

		if (digitsOnly === '') {
			inputValue = '';
			return;
		}

		const numericValue = Math.min(parseInt(digitsOnly, 10), MAX_VALUE);
		dispatch('change', numericValue);
		inputValue = formatNumber(numericValue);

		// Update content and move cursor to end after formatting
		requestAnimationFrame(() => {
			if (inputEl) {
				inputEl.textContent = inputValue;
				const range = document.createRange();
				const selection = window.getSelection();
				range.selectNodeContents(inputEl);
				range.collapse(false);
				selection.removeAllRanges();
				selection.addRange(range);
			}
		});
	}

	function handleBlur() {
		isEditing = false;
		if (inputValue !== '' && value === 0) {
			dispatch('change', 1);
		}
		inputValue = '';
	}

	function handleKeydown(event) {
		if (event.key === 'Enter') {
			event.preventDefault();
			event.target.blur();
		}
		const allowedKeys = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'];
		if (!allowedKeys.includes(event.key) && !/^[0-9]$/.test(event.key)) {
			event.preventDefault();
		}
	}
</script>

<div class="funding-target">
	<div class="funding-target__amount">
		<span
			bind:this={inputEl}
			contenteditable="true"
			inputmode="numeric"
			class="funding-target__number"
			role="textbox"
			aria-label="Funding target amount"
			on:input={handleInput}
			on:blur={handleBlur}
			on:keydown={handleKeydown}
		>{displayValue}</span>
		<span class="funding-target__bg" aria-hidden="true">{bgValue}</span>
	</div>
	<span class="funding-target__currency">&nbsp;€</span>
</div>
