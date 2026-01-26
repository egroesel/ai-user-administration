<script>
	import { createEventDispatcher } from 'svelte';

	export let value = 10000;
	export let selectedType = 'crowdfunding';

	const dispatch = createEventDispatcher();

	// Slider configuration
	const minValue = 1;
	const maxValue = 99999999;
	const exponent = 7;

	// Color mapping for each type
	// crowdfunding = green (#06E481), fundraising = pink (#FF85FF), private = yellow (#FFC21C)
	const colorClasses = {
		crowdfunding: {
			track: 'bg-[#06E481]',
			thumb: 'bg-[#06E481]'
		},
		fundraising: {
			track: 'bg-[#FF85FF]',
			thumb: 'bg-[#FF85FF]'
		},
		private: {
			track: 'bg-[#FFC21C]',
			thumb: 'bg-[#FFC21C]'
		}
	};

	$: colors = colorClasses[selectedType] || colorClasses.crowdfunding;

	// Convert amount to slider percentage (0-100)
	function amountToSlider(amount) {
		const range = maxValue - minValue;
		const normalized = (amount - minValue) / range;
		return Math.round(Math.pow(Math.max(0, normalized), 1 / exponent) * 100);
	}

	// Convert slider percentage to amount
	function sliderToAmount(sliderPercent) {
		const percentage = sliderPercent / 100;
		const range = maxValue - minValue;
		const rawAmount = minValue + range * Math.pow(percentage, exponent);
		return roundAmount(rawAmount);
	}

	// Smart rounding based on amount size
	function roundAmount(amount) {
		const thresholds = [
			[20, 1],
			[100, 5],
			[1000, 10],
			[10000, 100],
			[100000, 500],
			[1000000, 1000],
			[10000000, 10000],
			[99999999, 100000]
		];
		for (const [threshold, step] of thresholds) {
			if (amount < threshold) {
				return Math.round(amount / step) * step;
			}
		}
		return amount;
	}

	$: sliderPercent = amountToSlider(value);
	$: trackWidth = `${sliderPercent}%`;

	function handleSliderChange(event) {
		const newPercent = parseFloat(event.target.value);
		const newAmount = sliderToAmount(newPercent);
		dispatch('change', newAmount);
	}

	function handleInputChange(event) {
		const inputValue = event.target.value.replace(/[^0-9]/g, '');
		const numValue = parseInt(inputValue, 10) || 0;
		const clampedValue = Math.max(minValue, Math.min(maxValue, numValue));
		dispatch('change', clampedValue);
	}

	function formatCurrency(amount) {
		return new Intl.NumberFormat('de-DE', {
			style: 'decimal',
			minimumFractionDigits: 0,
			maximumFractionDigits: 0
		}).format(amount);
	}
</script>

<div class="w-full">
	<!-- Amount Input -->
	<div class="flex items-center justify-center mb-6">
		<div class="relative">
			<input
				type="text"
				value={formatCurrency(value)}
				on:change={handleInputChange}
				on:blur={handleInputChange}
				class="text-4xl md:text-5xl font-bold text-center text-[#304b50] dark:text-white bg-transparent border-none outline-none w-64 md:w-80"
			/>
			<span class="absolute right-0 top-1/2 -translate-y-1/2 text-4xl md:text-5xl font-bold text-[#304b50] dark:text-white">
				€
			</span>
		</div>
	</div>

	<!-- Slider -->
	<div class="relative h-6 mb-4">
		<!-- Track background -->
		<div class="absolute inset-y-0 left-0 right-0 my-auto h-6 bg-gray-200 dark:bg-gray-700 rounded-full"></div>

		<!-- Track filled -->
		<div
			class="absolute inset-y-0 left-0 my-auto h-6 rounded-full {colors.track}"
			style="width: {trackWidth}"
		></div>

		<!-- Range input -->
		<input
			type="range"
			min="0"
			max="100"
			step="0.1"
			value={sliderPercent}
			on:input={handleSliderChange}
			class="absolute inset-0 w-full h-6 appearance-none bg-transparent cursor-pointer slider-input"
			style="--thumb-color: {selectedType === 'crowdfunding'
				? '#06E481'
				: selectedType === 'fundraising'
					? '#FF85FF'
					: '#FFC21C'}"
		/>
	</div>

	<!-- Min/Max labels -->
	<div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
		<span>1 €</span>
		<span>99.999.999 €</span>
	</div>
</div>

<style>
	/* Custom slider styling */
	.slider-input::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: var(--thumb-color);
		cursor: pointer;
		border: 4px solid white;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.slider-input::-moz-range-thumb {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: var(--thumb-color);
		cursor: pointer;
		border: 4px solid white;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	.slider-input:focus::-webkit-slider-thumb {
		box-shadow: 0 0 0 4px rgba(6, 228, 129, 0.2);
	}

	.slider-input:focus::-moz-range-thumb {
		box-shadow: 0 0 0 4px rgba(6, 228, 129, 0.2);
	}
</style>
