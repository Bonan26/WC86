// WC86 - Wolf Club 86 Configuration
// Theme: Nightclub retro 80s avec des loups

const config = {
	// Premium Wolf Symbols
	symbols: {
		BOSS_WOLF: { id: 'BOSS_WOLF', type: 'premium' },
		HUSTLER: { id: 'HUSTLER', type: 'premium' },
		TECH_BRO: { id: 'TECH_BRO', type: 'premium' },
		DIAMOND_HANDS: { id: 'DIAMOND_HANDS', type: 'premium' },
		// Low Symbols (Club items)
		COCKTAIL: { id: 'COCKTAIL', type: 'low' },
		VIP_CARD: { id: 'VIP_CARD', type: 'low' },
		DISCO_BALL: { id: 'DISCO_BALL', type: 'low' },
		DICE: { id: 'DICE', type: 'low' },
		// Special Symbols
		ALPHA_WOLF: { id: 'ALPHA_WOLF', type: 'wild' },
		HOWLING_WILD: { id: 'HOWLING_WILD', type: 'wild' },
		MOON_SCATTER: { id: 'MOON_SCATTER', type: 'scatter' },
		TERRITORY: { id: 'TERRITORY', type: 'territory' },
	},

	// Bet modes
	betModes: {
		base: { cost: 1, type: 'standard' },
		pack_hunt: { cost: 75, type: 'buyBonus' },
		pack_hunt_plus: { cost: 150, type: 'buyBonus' },
		alpha_domination: { cost: 500, type: 'buyBonus' },
	},

	// Padding reels for different game types
	paddingReels: {
		basegame: 1,
		freegame: 1,
		alphaDomination: 1,
	},

	// Volatility modes
	volatilityModes: {
		LONE_WOLF: { rtp: 0.968, wincap: 10000, fsMultCap: 50 },
		PACK: { rtp: 0.965, wincap: 25000, fsMultCap: 200 },
		ALPHA: { rtp: 0.962, wincap: 50000, fsMultCap: 500 },
	},

	// Grid configurations
	gridConfigs: {
		'6x5': { reels: 6, rows: 5, ways: 7776 },
		'7x6': { reels: 7, rows: 6, ways: 46656 },
		'8x7': { reels: 8, rows: 7, ways: 117649 },
		'8x8': { reels: 8, rows: 8, ways: 262144 },
	},

	// Free spin triggers
	freeSpinTriggers: {
		basegame: { 3: 10, 4: 12, 5: 15, 6: 20 },
		freegame: { 2: 3, 3: 5, 4: 8, 5: 10, 6: 15 },
	},

	// Territory thresholds for grid expansion
	territoryThresholds: {
		3: '7x6',
		6: '8x7',
		10: '8x8',
	},
} as const;

export default config;
