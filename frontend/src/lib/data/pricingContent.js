/**
 * Static content for pricing plans
 * This replaces the Notion-fetched content from the original Vue app
 */

export const pricingContent = {
	de: {
		// Page titles
		titles: {
			selectType: 'Wähle deinen Projekttyp',
			selectFunding: 'Wie viel möchtest du einsammeln?',
			selectPlan: 'Wähle deinen Plan'
		},

		// Type descriptions
		types: {
			crowdfunding: {
				title: 'Crowdfunding',
				subtitle: 'Für kreative Projekte & Produkte',
				description:
					'Perfekt für Produktentwicklung, kreative Projekte, Events und alles, wo du deinen Unterstützern etwas zurückgeben kannst.'
			},
			fundraising: {
				title: 'Fundraising',
				subtitle: 'Für gemeinnützige Zwecke',
				description:
					'Ideal für Vereine, NGOs und soziale Projekte. Sammle Spenden für einen guten Zweck.'
			},
			private: {
				title: 'Privat',
				subtitle: 'Für persönliche Anlässe',
				description:
					'Für private Sammlungen wie Hochzeiten, Geburtstage oder besondere Lebensereignisse.'
			}
		},

		// Plan content
		plans: {
			basic: {
				name: 'Basic',
				subtitle: 'Für den Einstieg',
				shortDescription:
					'Alle grundlegenden Funktionen um dein Projekt zu starten. Perfekt für kleinere Projekte.',
				features: [
					'Projektseite erstellen',
					'Dankeschöns anlegen',
					'E-Mail Support',
					'Basis-Statistiken',
					'Social Media Sharing'
				],
				futureFeatures: ['Basis-Analyse-Tools', 'Standard-Templates'],
				paymentMethods: ['Kreditkarte', 'PayPal', 'SEPA-Lastschrift'],
				support: 'E-Mail Support (Mo-Fr)',
				cta: 'Mit Basic starten'
			},
			pro: {
				name: 'Pro',
				subtitle: 'Unser Bestseller',
				shortDescription:
					'Erweiterte Funktionen für ambitionierte Projekte. Mehr Reichweite, bessere Conversion.',
				features: [
					'Alles aus Basic',
					'Prioritäts-Support',
					'Erweiterte Statistiken',
					'Newsletter-Integration',
					'Custom Projektfarben',
					'Früher-Unterstützer-Bonus'
				],
				futureFeatures: ['A/B Testing für Dankeschöns', 'Retargeting Pixel Integration'],
				paymentMethods: ['Kreditkarte', 'PayPal', 'SEPA-Lastschrift', 'Klarna', 'Apple Pay'],
				support: 'Prioritäts-Support (Mo-Fr)',
				cta: 'Mit Pro starten'
			},
			premium: {
				name: 'Premium',
				subtitle: 'Maximaler Erfolg',
				shortDescription:
					'Alle Funktionen für maximalen Projekterfolg. Persönliche Betreuung inklusive.',
				features: [
					'Alles aus Pro',
					'Persönlicher Projektberater',
					'Marketing-Beratung',
					'Featured auf Startseite',
					'Presse-Unterstützung',
					'Dedizierter Account Manager'
				],
				futureFeatures: ['Exklusive Partner-Deals', 'Crowdfunding Academy Zugang'],
				paymentMethods: [
					'Kreditkarte',
					'PayPal',
					'SEPA-Lastschrift',
					'Klarna',
					'Apple Pay',
					'Google Pay',
					'Rechnung'
				],
				support: 'Persönlicher Support (7 Tage)',
				cta: 'Mit Premium starten'
			},
			enterprise: {
				name: 'Enterprise',
				subtitle: 'Auf Anfrage',
				shortDescription:
					'Maßgeschneiderte Lösungen für große Projekte und Unternehmen. Kontaktiere uns für ein individuelles Angebot.',
				features: [
					'Alles aus Premium',
					'Individuelle Provisionsvereinbarung',
					'White-Label Option',
					'API-Zugang',
					'Dediziertes Onboarding',
					'SLA-Garantie'
				],
				futureFeatures: [],
				paymentMethods: ['Alle Zahlungsmethoden', 'Individuelle Vereinbarungen'],
				support: '24/7 Premium Support',
				cta: 'Kontakt aufnehmen'
			}
		},

		// Labels & misc
		labels: {
			recommended: 'Empfohlen',
			provision: 'Provision',
			ongoingCost: 'Laufende Kosten',
			onDemand: 'Auf Anfrage',
			showMore: 'Mehr anzeigen',
			showLess: 'Weniger anzeigen',
			features: 'Funktionen',
			futureFeatures: 'Demnächst verfügbar',
			paymentMethods: 'Zahlungsarten',
			support: 'Support',
			voucherTitle: 'Hast du einen Gutschein?',
			voucherPlaceholder: 'Gutscheincode eingeben',
			voucherApply: 'Einlösen',
			voucherApplied: 'Gutschein angewendet',
			voucherInvalid: 'Ungültiger Gutscheincode',
			voucherTypeError: 'Dieser Gutschein gilt nicht für diesen Projekttyp',
			discountApplied: 'Rabatt angewendet',
			fundingGoalLabel: 'Gewünschtes Finanzierungsziel',
			fundingResultText:
				'Um %targetAmount% € zu erhalten, benötigst du bei %provision% % Provision ein Finanzierungsziel von %calculatedAmount% €.',
			tierDiscount: 'Bei diesem Betrag erhältst du einen Mengenrabatt von %discount% %.',
			voucherSaving: 'Mit deinem Gutschein sparst du %saving% €.',
			continueButton: 'Weiter zum Projekt',
			backButton: 'Zurück',
			notAvailable: 'Nicht verfügbar für diesen Projekttyp',
			businessOffer:
				'Du planst ein größeres Projekt? Kontaktiere uns für ein individuelles Angebot.'
		},

		// Sum calculator
		calculator: {
			title: 'Wie viel möchtest du einsammeln?',
			subtitle: 'Schiebe den Regler oder gib einen Betrag ein',
			result:
				'Bei %provision% % Provision erhältst du ca. %netAmount% € nach Abzug aller Gebühren.',
			tierInfo: 'Ab %threshold% € erhältst du %discount% % Mengenrabatt auf die Provision.'
		}
	},

	en: {
		// Page titles
		titles: {
			selectType: 'Choose your project type',
			selectFunding: 'How much do you want to raise?',
			selectPlan: 'Choose your plan'
		},

		// Type descriptions
		types: {
			crowdfunding: {
				title: 'Crowdfunding',
				subtitle: 'For creative projects & products',
				description:
					'Perfect for product development, creative projects, events, and anything where you can give back to your supporters.'
			},
			fundraising: {
				title: 'Fundraising',
				subtitle: 'For charitable causes',
				description:
					'Ideal for associations, NGOs, and social projects. Collect donations for a good cause.'
			},
			private: {
				title: 'Private',
				subtitle: 'For personal occasions',
				description:
					'For private collections like weddings, birthdays, or special life events.'
			}
		},

		// Plan content
		plans: {
			basic: {
				name: 'Basic',
				subtitle: 'For getting started',
				shortDescription:
					'All the basic features to launch your project. Perfect for smaller projects.',
				features: [
					'Create project page',
					'Set up rewards',
					'Email support',
					'Basic statistics',
					'Social media sharing'
				],
				futureFeatures: ['Basic analytics tools', 'Standard templates'],
				paymentMethods: ['Credit card', 'PayPal', 'SEPA Direct Debit'],
				support: 'Email support (Mon-Fri)',
				cta: 'Start with Basic'
			},
			pro: {
				name: 'Pro',
				subtitle: 'Our bestseller',
				shortDescription:
					'Advanced features for ambitious projects. More reach, better conversion.',
				features: [
					'Everything from Basic',
					'Priority support',
					'Advanced statistics',
					'Newsletter integration',
					'Custom project colors',
					'Early supporter bonus'
				],
				futureFeatures: ['A/B testing for rewards', 'Retargeting pixel integration'],
				paymentMethods: ['Credit card', 'PayPal', 'SEPA Direct Debit', 'Klarna', 'Apple Pay'],
				support: 'Priority support (Mon-Fri)',
				cta: 'Start with Pro'
			},
			premium: {
				name: 'Premium',
				subtitle: 'Maximum success',
				shortDescription:
					'All features for maximum project success. Personal support included.',
				features: [
					'Everything from Pro',
					'Personal project advisor',
					'Marketing consultation',
					'Featured on homepage',
					'Press support',
					'Dedicated account manager'
				],
				futureFeatures: ['Exclusive partner deals', 'Crowdfunding Academy access'],
				paymentMethods: [
					'Credit card',
					'PayPal',
					'SEPA Direct Debit',
					'Klarna',
					'Apple Pay',
					'Google Pay',
					'Invoice'
				],
				support: 'Personal support (7 days)',
				cta: 'Start with Premium'
			},
			enterprise: {
				name: 'Enterprise',
				subtitle: 'On request',
				shortDescription:
					'Customized solutions for large projects and companies. Contact us for a personalized offer.',
				features: [
					'Everything from Premium',
					'Custom commission agreement',
					'White-label option',
					'API access',
					'Dedicated onboarding',
					'SLA guarantee'
				],
				futureFeatures: [],
				paymentMethods: ['All payment methods', 'Individual agreements'],
				support: '24/7 Premium Support',
				cta: 'Contact us'
			}
		},

		// Labels & misc
		labels: {
			recommended: 'Recommended',
			provision: 'Commission',
			ongoingCost: 'Ongoing costs',
			onDemand: 'On request',
			showMore: 'Show more',
			showLess: 'Show less',
			features: 'Features',
			futureFeatures: 'Coming soon',
			paymentMethods: 'Payment methods',
			support: 'Support',
			voucherTitle: 'Do you have a voucher?',
			voucherPlaceholder: 'Enter voucher code',
			voucherApply: 'Apply',
			voucherApplied: 'Voucher applied',
			voucherInvalid: 'Invalid voucher code',
			voucherTypeError: "This voucher doesn't apply to this project type",
			discountApplied: 'Discount applied',
			fundingGoalLabel: 'Desired funding goal',
			fundingResultText:
				'To receive %targetAmount% €, you need a funding goal of %calculatedAmount% € at %provision% % commission.',
			tierDiscount: 'At this amount, you receive a volume discount of %discount% %.',
			voucherSaving: 'With your voucher you save %saving% €.',
			continueButton: 'Continue to project',
			backButton: 'Back',
			notAvailable: 'Not available for this project type',
			businessOffer: 'Planning a larger project? Contact us for a custom offer.'
		},

		// Sum calculator
		calculator: {
			title: 'How much do you want to raise?',
			subtitle: 'Use the slider or enter an amount',
			result:
				'At %provision% % commission, you will receive approx. %netAmount% € after all fees.',
			tierInfo: 'From %threshold% € you receive %discount% % volume discount on the commission.'
		}
	}
};

/**
 * Get content for a specific language
 * @param {string} lang - Language code ('de' or 'en')
 * @returns {object} Content object
 */
export function getPricingContent(lang = 'de') {
	return pricingContent[lang] || pricingContent.de;
}

/**
 * Get plan content by key
 * @param {string} planKey - Plan key (basic, pro, premium, enterprise)
 * @param {string} lang - Language code
 * @returns {object} Plan content
 */
export function getPlanContent(planKey, lang = 'de') {
	const content = getPricingContent(lang);
	return content.plans[planKey] || null;
}

/**
 * Get type content by key
 * @param {string} typeKey - Type key (crowdfunding, fundraising, private)
 * @param {string} lang - Language code
 * @returns {object} Type content
 */
export function getTypeContent(typeKey, lang = 'de') {
	const content = getPricingContent(lang);
	return content.types[typeKey] || null;
}
