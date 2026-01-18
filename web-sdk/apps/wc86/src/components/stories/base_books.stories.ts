import type { Meta, StoryObj } from '@storybook/svelte';

// Story metadata
const meta = {
	title: 'WC86/Base Game Books',
	tags: ['autodocs'],
	parameters: {
		layout: 'fullscreen',
	},
} satisfies Meta;

export default meta;
type Story = StoryObj<typeof meta>;

// Basic reveal story
export const BasicReveal: Story = {
	name: 'Basic Reveal',
	parameters: {
		docs: {
			description: {
				story: 'Shows a basic board reveal with premium and low symbols.',
			},
		},
	},
};

// Win story
export const SimpleWin: Story = {
	name: 'Simple Win',
	parameters: {
		docs: {
			description: {
				story: 'Shows a simple 3-of-a-kind win with Boss Wolf.',
			},
		},
	},
};

// Cascade win
export const CascadeWin: Story = {
	name: 'Cascade Win',
	parameters: {
		docs: {
			description: {
				story: 'Shows multiple cascade wins with hunt multiplier increasing.',
			},
		},
	},
};

// Wild landing
export const WildLanding: Story = {
	name: 'Wild Landing',
	parameters: {
		docs: {
			description: {
				story: 'Shows Alpha Wolf wild symbol landing animation.',
			},
		},
	},
};

// Howling Wild with multiplier
export const HowlingWildMultiplier: Story = {
	name: 'Howling Wild Multiplier',
	parameters: {
		docs: {
			description: {
				story: 'Shows Howling Wild landing with random multiplier.',
			},
		},
	},
};
