import type { Meta, StoryObj } from '@storybook/svelte';

// Story metadata
const meta = {
	title: 'WC86/Bonus Features',
	tags: ['autodocs'],
	parameters: {
		layout: 'fullscreen',
	},
} satisfies Meta;

export default meta;
type Story = StoryObj<typeof meta>;

// Pack Split feature
export const PackSplit: Story = {
	name: 'Pack Split',
	parameters: {
		docs: {
			description: {
				story: 'Alpha Wolf splits and duplicates symbols to the left with x2, x3, or x4 multiplier.',
			},
		},
	},
};

// Howl Chain feature
export const HowlChain: Story = {
	name: 'Howl Chain',
	parameters: {
		docs: {
			description: {
				story: 'Adjacent Howling Wilds create chain connections. 2 wilds = additive, 3+ = multiplicative.',
			},
		},
	},
};

// Territory Expansion
export const TerritoryExpand: Story = {
	name: 'Territory Expansion',
	parameters: {
		docs: {
			description: {
				story: 'Collect 3/6/10 Territory symbols to expand the grid from 6x5 to 7x6, 8x7, or 8x8.',
			},
		},
	},
};

// Free Spins Trigger
export const FreeSpinsTrigger: Story = {
	name: 'Pack Hunt Trigger',
	parameters: {
		docs: {
			description: {
				story: '3+ Moon Scatter symbols trigger Pack Hunt free spins mode.',
			},
		},
	},
};

// Free Spins Session
export const FreeSpinsSession: Story = {
	name: 'Pack Hunt Session',
	parameters: {
		docs: {
			description: {
				story: 'Full Pack Hunt free spins session with persistent multiplier.',
			},
		},
	},
};

// Alpha Domination
export const AlphaDomination: Story = {
	name: 'Alpha Domination',
	parameters: {
		docs: {
			description: {
				story: 'Super bonus mode with 8x8 grid, starting multiplier x5, and max multiplier x500.',
			},
		},
	},
};

// Big Win
export const BigWin: Story = {
	name: 'Big Win',
	parameters: {
		docs: {
			description: {
				story: 'Big win celebration animation with coin particles.',
			},
		},
	},
};

// Max Win
export const MaxWin: Story = {
	name: 'Max Win',
	parameters: {
		docs: {
			description: {
				story: 'Maximum win celebration (10,000x / 25,000x / 50,000x depending on volatility mode).',
			},
		},
	},
};
