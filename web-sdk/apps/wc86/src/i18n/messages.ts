import en from './en.json';
import fr from './fr.json';

export type Locale = 'en' | 'fr';

export const messages = {
	en,
	fr
} as const;

export type Messages = typeof en;

let currentLocale: Locale = 'en';

/**
 * Set the current locale
 */
export function setLocale(locale: Locale): void {
	if (messages[locale]) {
		currentLocale = locale;
	} else {
		console.warn(`Locale "${locale}" not found, falling back to "en"`);
		currentLocale = 'en';
	}
}

/**
 * Get the current locale
 */
export function getLocale(): Locale {
	return currentLocale;
}

/**
 * Get all available locales
 */
export function getAvailableLocales(): Locale[] {
	return Object.keys(messages) as Locale[];
}

/**
 * Get a translated message by key path
 * @param key - Dot-notation path to the message (e.g., 'game.title')
 * @param params - Optional parameters for interpolation
 */
export function t(key: string, params?: Record<string, string | number>): string {
	const keys = key.split('.');
	let value: unknown = messages[currentLocale];

	for (const k of keys) {
		if (value && typeof value === 'object' && k in value) {
			value = (value as Record<string, unknown>)[k];
		} else {
			console.warn(`Translation key "${key}" not found for locale "${currentLocale}"`);
			return key;
		}
	}

	if (typeof value !== 'string') {
		console.warn(`Translation key "${key}" does not resolve to a string`);
		return key;
	}

	// Handle interpolation
	if (params) {
		return value.replace(/\{\{(\w+)\}\}/g, (_, paramKey) => {
			return params[paramKey]?.toString() ?? `{{${paramKey}}}`;
		});
	}

	return value;
}

/**
 * Create a reactive translation function for Svelte
 */
export function createTranslator(locale: Locale = 'en') {
	setLocale(locale);
	return t;
}

/**
 * Format a number according to locale
 */
export function formatNumber(value: number, locale: Locale = currentLocale): string {
	return new Intl.NumberFormat(locale).format(value);
}

/**
 * Format currency according to locale
 */
export function formatCurrency(
	value: number,
	currency: string = 'USD',
	locale: Locale = currentLocale
): string {
	return new Intl.NumberFormat(locale, {
		style: 'currency',
		currency
	}).format(value);
}

export default {
	messages,
	t,
	setLocale,
	getLocale,
	getAvailableLocales,
	createTranslator,
	formatNumber,
	formatCurrency
};
