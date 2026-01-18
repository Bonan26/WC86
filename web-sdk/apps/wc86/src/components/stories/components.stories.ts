import type { Meta, StoryObj } from '@storybook/svelte';

// Story metadata
const meta = {
	title: 'WC86/Components',
	tags: ['autodocs'],
	parameters: {
		layout: 'centered',
	},
} satisfies Meta;

export default meta;
type Story = StoryObj<typeof meta>;

// Hunt Multiplier Component
export const HuntMultiplier: Story = {
	name: 'Hunt Multiplier',
	parameters: {
		docs: {
			description: {
				story: 'Displays the current hunt cascade multiplier. Increases by +1 with each cascade.',
			},
		},
	},
};

// Territory Progress
export const TerritoryProgress: Story = {
	name: 'Territory Progress',
	parameters: {
		docs: {
			description: {
				story: 'Progress bar showing collected territory symbols and next grid expansion threshold.',
			},
		},
	},
};

// Volatility Selector
export const VolatilitySelector: Story = {
	name: 'Volatility Selector',
	parameters: {
		docs: {
			description: {
				story: 'Player selection UI for choosing between LONE_WOLF, PACK, or ALPHA volatility modes.',
			},
		},
	},
};

// Symbol Gallery
export const SymbolGallery: Story = {
	name: 'Symbol Gallery',
	parameters: {
		docs: {
			description: {
				story: 'All 12 WC86 symbols: 4 premium wolves, 4 low club items, and 4 special symbols.',
			},
		},
	},
};

// Free Spin Counter
export const FreeSpinCounter: Story = {
	name: 'Free Spin Counter',
	parameters: {
		docs: {
			description: {
				story: 'Pack Hunt free spins counter showing current spin and total spins.',
			},
		},
	},
};

// Loading Screen
export const LoadingScreen: Story = {
	name: 'Loading Screen',
	parameters: {
		docs: {
			description: {
				story: 'Wolf Club 86 loading screen with animated logo and progress bar.',
			},
		},
	},
};

// Backgrounds
export const Backgrounds: Story = {
	name: 'Background Variants',
	parameters: {
		docs: {
			description: {
				story: 'Three background variants: Base game (nightclub entrance), Pack Hunt (inside club), Alpha Domination (VIP area).',
			},
		},
	},
};
