<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import '$lib/styles/input-start-date.scss';

	export let value = '';
	export let selectedType = 'crowdfunding';

	const dispatch = createEventDispatcher();

	let datePickerDate = '';

	// Calculate dates
	$: today = getToday();
	$: initialDate = getInitialDate();
	$: maxDate = getMaxDate();

	function getToday() {
		const d = new Date();
		if (d.getMinutes() > 0 || d.getSeconds() > 0 || d.getMilliseconds() > 0) {
			d.setHours(d.getHours() + 1);
		}
		d.setMinutes(0, 0, 0);
		return formatDate(d);
	}

	function getInitialDate() {
		const d = new Date();
		d.setDate(d.getDate() + 14);
		d.setHours(10, 0, 0, 0);
		return formatDate(d);
	}

	function getMaxDate() {
		const d = new Date();
		d.setFullYear(d.getFullYear() + 5);
		return formatDate(d);
	}

	function formatDate(d) {
		const pad = (n) => String(n).padStart(2, '0');
		return (
			d.getFullYear() +
			'-' + pad(d.getMonth() + 1) +
			'-' + pad(d.getDate()) +
			'T' + pad(d.getHours()) +
			':' + pad(d.getMinutes())
		);
	}

	function openPicker(e) {
		if (e.target.showPicker) {
			e.target.showPicker();
		}
	}

	function removeSecondsFromDate() {
		const d = new Date(datePickerDate);
		d.setMinutes(0, 0, 0);
		datePickerDate = formatDate(d);
	}

	function handleDateInput() {
		if (datePickerDate) {
			removeSecondsFromDate();

			// Validation for min/max
			if (datePickerDate < today) {
				datePickerDate = today;
				return;
			}
			if (datePickerDate > maxDate) {
				datePickerDate = maxDate;
				return;
			}

			dispatch('change', datePickerDate);
		} else {
			// If date is removed, reset to initial date
			datePickerDate = initialDate;
			dispatch('change', datePickerDate);
		}
	}

	onMount(() => {
		// Use provided value or set initial date
		if (value) {
			datePickerDate = value;
		} else {
			datePickerDate = initialDate;
			dispatch('change', datePickerDate);
		}
	});
</script>

<div class="input-start-date">
	<input
		class="input-start-date__native-date-input"
		type="datetime-local"
		step="3600"
		min={today}
		max={maxDate}
		bind:value={datePickerDate}
		on:click={openPicker}
		on:change={handleDateInput}
	/>
</div>
