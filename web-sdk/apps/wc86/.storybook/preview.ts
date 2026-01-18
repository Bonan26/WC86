import type { Preview } from '@storybook/svelte';

const preview: Preview = {
	parameters: {
		actions: { argTypesRegex: '^on[A-Z].*' },
		controls: {
			matchers: {
				color: /(background|color)$/i,
				date: /Date$/i,
			},
		},
		backgrounds: {
			default: 'dark',
			values: [
				{ name: 'dark', value: '#0a0a14' },
				{ name: 'light', value: '#f5f5f5' },
				{ name: 'nightclub', value: '#1a0a2e' },
			],
		},
	},
};

export default preview;
