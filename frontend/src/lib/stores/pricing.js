import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

// Product definitions with provisions per type
const PRODUCT_DEFINITIONS = {
	basic: {
		key: 'basic',
		types: ['fundraising', 'crowdfunding', 'private'],
		scopes: {
			crowdfunding: { provision: 9, scope: 1 },
			fundraising: { provision: 5, scope: 1 },
			private: { provision: 4, scope: 1 }
		}
	},
	pro: {
		key: 'pro',
		types: ['fundraising', 'crowdfunding', 'private'],
		scopes: {
			crowdfunding: { provision: 7, scope: 2 },
			fundraising: { provision: 4, scope: 2 },
			private: { provision: 3, scope: 2 }
		}
	},
	premium: {
		key: 'premium',
		types: ['fundraising', 'crowdfunding', 'private'],
		scopes: {
			crowdfunding: { provision: 5, scope: 3 },
			fundraising: { provision: 3, scope: 3 },
			private: { provision: 2, scope: 3 }
		}
	},
	enterprise: {
		key: 'enterprise',
		types: ['fundraising', 'crowdfunding'],
		isOnDemand: true,
		scopes: {
			crowdfunding: { provision: null, scope: 4 },
			fundraising: { provision: null, scope: 4 }
		}
	}
};

// Default funding targets per type
const DEFAULT_FUNDING_TARGETS = {
	crowdfunding: 50000,
	fundraising: 25000,
	private: 500
};

// Discount tiers for large funding goals
const DISCOUNT_TIERS = [
	{ threshold: 0, discount: 0 },
	{ threshold: 25000, discount: 5 },
	{ threshold: 50000, discount: 15 },
	{ threshold: 100000, discount: 20 },
	{ threshold: 500000, discount: 35 },
	{ threshold: 1000000, discount: 50 }
];

function createPricingStore() {
	const { subscribe, set, update } = writable({
		selectedType: 'crowdfunding',
		selectedPlan: 'pro',
		fundingGoal: DEFAULT_FUNDING_TARGETS.crowdfunding,
		voucher: {
			code: '',
			discount: 0,
			isValid: false,
			forPlans: []
		}
	});

	function setType(type) {
		update((state) => {
			// Reset plan based on type
			let newPlan = state.selectedPlan;
			if (type === 'private' && state.selectedPlan === 'enterprise') {
				newPlan = 'basic';
			} else if (type === 'private') {
				newPlan = 'basic';
			} else {
				newPlan = 'pro';
			}

			return {
				...state,
				selectedType: type,
				selectedPlan: newPlan,
				fundingGoal: DEFAULT_FUNDING_TARGETS[type],
				voucher: { code: '', discount: 0, isValid: false, forPlans: [] }
			};
		});
	}

	function setPlan(plan) {
		update((state) => ({ ...state, selectedPlan: plan }));
	}

	function setFundingGoal(goal) {
		update((state) => ({ ...state, fundingGoal: goal }));
	}

	function setVoucher(voucher) {
		update((state) => ({
			...state,
			voucher: {
				code: voucher.code || '',
				discount: voucher.discount || 0,
				isValid: voucher.isValid || false,
				forPlans: voucher.forPlans || []
			}
		}));
	}

	function resetVoucher() {
		update((state) => ({
			...state,
			voucher: { code: '', discount: 0, isValid: false, forPlans: [] }
		}));
	}

	function reset() {
		set({
			selectedType: 'crowdfunding',
			selectedPlan: 'pro',
			fundingGoal: DEFAULT_FUNDING_TARGETS.crowdfunding,
			voucher: { code: '', discount: 0, isValid: false, forPlans: [] }
		});
	}

	return {
		subscribe,
		setType,
		setPlan,
		setFundingGoal,
		setVoucher,
		resetVoucher,
		reset
	};
}

export const pricing = createPricingStore();

// Derived store for products with calculated provisions
export const products = derived(pricing, ($pricing) => {
	const { selectedType, voucher } = $pricing;

	return Object.entries(PRODUCT_DEFINITIONS).map(([key, product]) => {
		const scope = product.scopes[selectedType];
		const isAvailable = product.types.includes(selectedType);
		const isOnDemand = product.isOnDemand || false;

		let provision = scope?.provision ?? null;
		let discountedProvision = provision;

		// Apply voucher discount if valid for this plan
		if (voucher.isValid && voucher.discount > 0 && provision !== null) {
			if (voucher.forPlans.length === 0 || voucher.forPlans.includes(key)) {
				discountedProvision = provision * (1 - voucher.discount / 100);
			}
		}

		return {
			key,
			isAvailable,
			isOnDemand,
			provision,
			discountedProvision,
			scope: scope?.scope
		};
	});
});

// Derived store for selected product details
export const selectedProduct = derived(pricing, ($pricing) => {
	const { selectedType, selectedPlan, fundingGoal, voucher } = $pricing;
	const product = PRODUCT_DEFINITIONS[selectedPlan];

	if (!product) return null;

	const scope = product.scopes[selectedType];
	const provision = scope?.provision ?? null;

	let discountedProvision = provision;
	if (voucher.isValid && voucher.discount > 0 && provision !== null) {
		if (voucher.forPlans.length === 0 || voucher.forPlans.includes(selectedPlan)) {
			discountedProvision = provision * (1 - voucher.discount / 100);
		}
	}

	return {
		plan: selectedPlan,
		type: selectedType,
		fundingGoal,
		provision,
		discountedProvision,
		scope: scope?.scope,
		voucherCode: voucher.isValid ? voucher.code : null,
		voucherDiscount: voucher.isValid ? voucher.discount : 0
	};
});

// Helper functions
export function isPlanAvailable(plan, type) {
	return PRODUCT_DEFINITIONS[plan]?.types.includes(type) ?? false;
}

export function getDiscountTier(amount) {
	for (let i = DISCOUNT_TIERS.length - 1; i >= 0; i--) {
		if (amount >= DISCOUNT_TIERS[i].threshold) {
			return DISCOUNT_TIERS[i];
		}
	}
	return DISCOUNT_TIERS[0];
}

export function calculateEffectiveProvision(amount, baseProvision) {
	const tier = getDiscountTier(amount);
	return baseProvision * (1 - tier.discount / 100);
}

export { PRODUCT_DEFINITIONS, DEFAULT_FUNDING_TARGETS, DISCOUNT_TIERS };
