import type { RawSymbol, SymbolState, GridSize } from './types';

export const SYMBOL_SIZE = 120;
export const REEL_PADDING = 0.53;

// Grid configurations
export const GRID_CONFIGS = {
	'6x5': { reels: 6, rows: 5, ways: 7776 },
	'7x6': { reels: 7, rows: 6, ways: 46656 },
	'8x7': { reels: 8, rows: 7, ways: 117649 },
	'8x8': { reels: 8, rows: 8, ways: 262144 },
} as const;

// Default grid (6x5)
export const DEFAULT_GRID: GridSize = '6x5';
export const BOARD_DIMENSIONS = { x: 6, y: 5 };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

// Initial board for 6x5 grid (padded top and bottom)
export const INITIAL_BOARD: RawSymbol[][] = [
	[
		{ name: 'BOSS_WOLF' },
		{ name: 'COCKTAIL' },
		{ name: 'DISCO_BALL' },
		{ name: 'DICE' },
		{ name: 'VIP_CARD' },
	],
	[
		{ name: 'HUSTLER' },
		{ name: 'VIP_CARD' },
		{ name: 'COCKTAIL' },
		{ name: 'DISCO_BALL' },
		{ name: 'DICE' },
	],
	[
		{ name: 'TECH_BRO' },
		{ name: 'DICE' },
		{ name: 'VIP_CARD' },
		{ name: 'COCKTAIL' },
		{ name: 'DISCO_BALL' },
	],
	[
		{ name: 'DIAMOND_HANDS' },
		{ name: 'DISCO_BALL' },
		{ name: 'DICE' },
		{ name: 'VIP_CARD' },
		{ name: 'COCKTAIL' },
	],
	[
		{ name: 'COCKTAIL' },
		{ name: 'BOSS_WOLF' },
		{ name: 'HUSTLER' },
		{ name: 'TECH_BRO' },
		{ name: 'DIAMOND_HANDS' },
	],
	[
		{ name: 'VIP_CARD' },
		{ name: 'DICE' },
		{ name: 'DISCO_BALL' },
		{ name: 'COCKTAIL' },
		{ name: 'BOSS_WOLF' },
	],
];

// Background ratios
export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;

export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

// Symbol categories
export const PREMIUM_SYMBOLS = ['BOSS_WOLF', 'HUSTLER', 'TECH_BRO', 'DIAMOND_HANDS'];
export const LOW_SYMBOLS = ['COCKTAIL', 'VIP_CARD', 'DISCO_BALL', 'DICE'];
export const WILD_SYMBOLS = ['ALPHA_WOLF', 'HOWLING_WILD'];
export const SCATTER_SYMBOLS = ['MOON_SCATTER'];
export const TERRITORY_SYMBOLS = ['TERRITORY'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

// Symbol size ratios
const PREMIUM_SYMBOL_SIZE = 0.9;
const LOW_SYMBOL_SIZE = 0.85;
const SPECIAL_SYMBOL_SIZE = 1;
const WILD_SYMBOL_SIZE = 1.1;

// Spin options
const SPIN_OPTIONS_SHARED = {
	reelFallInDelay: 80,
	reelPaddingMultiplierNormal: 1.25,
	reelPaddingMultiplierAnticipated: 18,
	reelFallOutDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	symbolFallInSpeed: 3.5,
	symbolFallInInterval: 30,
	symbolFallInBounceSpeed: 0.15,
	symbolFallInBounceSizeMulti: 0.5,
	symbolFallOutSpeed: 3.5,
	symbolFallOutInterval: 20,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	symbolFallInSpeed: 7,
	symbolFallInInterval: 0,
	symbolFallInBounceSpeed: 0.3,
	symbolFallInBounceSizeMulti: 0.25,
	symbolFallOutSpeed: 7,
	symbolFallOutInterval: 0,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

// Explosion animation (shared)
const explosion = {
	type: 'spine',
	assetKey: 'explosion',
	animationName: 'explosion',
	sizeRatios: { width: 1, height: 1 },
};

// Premium Wolf Symbols
const bossWolfStatic = { type: 'sprite', assetKey: 'boss_wolf.webp', sizeRatios: { width: 1, height: 1 } };
const hustlerStatic = { type: 'sprite', assetKey: 'hustler.webp', sizeRatios: { width: 1, height: 1 } };
const techBroStatic = { type: 'sprite', assetKey: 'tech_bro.webp', sizeRatios: { width: 1, height: 1 } };
const diamondHandsStatic = { type: 'sprite', assetKey: 'diamond_hands.webp', sizeRatios: { width: 1, height: 1 } };

// Low Symbols (Club items)
const cocktailStatic = { type: 'sprite', assetKey: 'cocktail.webp', sizeRatios: { width: 1, height: 1 } };
const vipCardStatic = { type: 'sprite', assetKey: 'vip_card.webp', sizeRatios: { width: 1, height: 1 } };
const discoBallStatic = { type: 'sprite', assetKey: 'disco_ball.webp', sizeRatios: { width: 1, height: 1 } };
const diceStatic = { type: 'sprite', assetKey: 'dice.webp', sizeRatios: { width: 1, height: 1 } };

// Special Symbols
const alphaWolfStatic = { type: 'sprite', assetKey: 'alpha_wolf.webp', sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE } };
const howlingWildStatic = { type: 'sprite', assetKey: 'howling_wild.webp', sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE } };
const moonScatterStatic = { type: 'sprite', assetKey: 'moon_scatter.webp', sizeRatios: { width: SPECIAL_SYMBOL_SIZE * 1.2, height: SPECIAL_SYMBOL_SIZE * 1.2 } };
const territoryStatic = { type: 'sprite', assetKey: 'territory.webp', sizeRatios: { width: 1, height: 1 } };

// Symbol Info Map for WC86
export const SYMBOL_INFO_MAP = {
	// Premium Wolves
	BOSS_WOLF: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'boss_wolf',
			animationName: 'win',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
		postWinStatic: bossWolfStatic,
		static: bossWolfStatic,
		spin: bossWolfStatic,
		land: {
			type: 'spine',
			assetKey: 'boss_wolf',
			animationName: 'land',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
	},
	HUSTLER: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'hustler',
			animationName: 'win',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
		postWinStatic: hustlerStatic,
		static: hustlerStatic,
		spin: hustlerStatic,
		land: {
			type: 'spine',
			assetKey: 'hustler',
			animationName: 'land',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
	},
	TECH_BRO: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'tech_bro',
			animationName: 'win',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
		postWinStatic: techBroStatic,
		static: techBroStatic,
		spin: techBroStatic,
		land: {
			type: 'spine',
			assetKey: 'tech_bro',
			animationName: 'land',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
	},
	DIAMOND_HANDS: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'diamond_hands',
			animationName: 'win',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
		postWinStatic: diamondHandsStatic,
		static: diamondHandsStatic,
		spin: diamondHandsStatic,
		land: {
			type: 'spine',
			assetKey: 'diamond_hands',
			animationName: 'land',
			sizeRatios: { width: PREMIUM_SYMBOL_SIZE, height: PREMIUM_SYMBOL_SIZE },
		},
	},
	// Low Symbols (Club items)
	COCKTAIL: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'cocktail',
			animationName: 'win',
			sizeRatios: { width: LOW_SYMBOL_SIZE, height: LOW_SYMBOL_SIZE },
		},
		postWinStatic: cocktailStatic,
		static: cocktailStatic,
		spin: cocktailStatic,
		land: cocktailStatic,
	},
	VIP_CARD: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'vip_card',
			animationName: 'win',
			sizeRatios: { width: LOW_SYMBOL_SIZE, height: LOW_SYMBOL_SIZE },
		},
		postWinStatic: vipCardStatic,
		static: vipCardStatic,
		spin: vipCardStatic,
		land: vipCardStatic,
	},
	DISCO_BALL: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'disco_ball',
			animationName: 'win',
			sizeRatios: { width: LOW_SYMBOL_SIZE, height: LOW_SYMBOL_SIZE },
		},
		postWinStatic: discoBallStatic,
		static: discoBallStatic,
		spin: discoBallStatic,
		land: discoBallStatic,
	},
	DICE: {
		explosion,
		win: {
			type: 'spine',
			assetKey: 'dice',
			animationName: 'win',
			sizeRatios: { width: LOW_SYMBOL_SIZE, height: LOW_SYMBOL_SIZE },
		},
		postWinStatic: diceStatic,
		static: diceStatic,
		spin: diceStatic,
		land: diceStatic,
	},
	// Special Symbols
	ALPHA_WOLF: {
		explosion,
		postWinStatic: alphaWolfStatic,
		static: alphaWolfStatic,
		spin: alphaWolfStatic,
		win: {
			type: 'spine',
			assetKey: 'alpha_wolf',
			animationName: 'win',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
		land: {
			type: 'spine',
			assetKey: 'alpha_wolf',
			animationName: 'land',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
		split: {
			type: 'spine',
			assetKey: 'alpha_wolf',
			animationName: 'split',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
	},
	HOWLING_WILD: {
		explosion,
		postWinStatic: howlingWildStatic,
		static: howlingWildStatic,
		spin: howlingWildStatic,
		win: {
			type: 'spine',
			assetKey: 'howling_wild',
			animationName: 'win',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
		land: {
			type: 'spine',
			assetKey: 'howling_wild',
			animationName: 'land',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
		howl: {
			type: 'spine',
			assetKey: 'howling_wild',
			animationName: 'howl',
			sizeRatios: { width: WILD_SYMBOL_SIZE, height: WILD_SYMBOL_SIZE },
		},
	},
	MOON_SCATTER: {
		explosion,
		postWinStatic: moonScatterStatic,
		static: moonScatterStatic,
		spin: {
			type: 'spine',
			assetKey: 'moon_scatter',
			animationName: 'spin',
			sizeRatios: { width: SPECIAL_SYMBOL_SIZE * 1.5, height: SPECIAL_SYMBOL_SIZE * 1.5 },
		},
		win: {
			type: 'spine',
			assetKey: 'moon_scatter',
			animationName: 'win',
			sizeRatios: { width: SPECIAL_SYMBOL_SIZE * 1.5, height: SPECIAL_SYMBOL_SIZE * 1.5 },
		},
		land: {
			type: 'spine',
			assetKey: 'moon_scatter',
			animationName: 'land',
			sizeRatios: { width: SPECIAL_SYMBOL_SIZE * 1.5, height: SPECIAL_SYMBOL_SIZE * 1.5 },
		},
	},
	TERRITORY: {
		explosion,
		postWinStatic: territoryStatic,
		static: territoryStatic,
		spin: territoryStatic,
		win: {
			type: 'spine',
			assetKey: 'territory',
			animationName: 'win',
			sizeRatios: { width: 1, height: 1 },
		},
		land: {
			type: 'spine',
			assetKey: 'territory',
			animationName: 'land',
			sizeRatios: { width: 1, height: 1 },
		},
		glow: {
			type: 'spine',
			assetKey: 'territory',
			animationName: 'glow',
			sizeRatios: { width: 1, height: 1 },
		},
	},
} as const;

// Sound mappings
export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_land_1',
	2: 'sfx_scatter_land_2',
	3: 'sfx_scatter_land_3',
	4: 'sfx_scatter_land_4',
	5: 'sfx_scatter_land_5',
	6: 'sfx_scatter_land_6',
} as const;

export const TERRITORY_LAND_SOUND_MAP = {
	1: 'sfx_territory_land_1',
	2: 'sfx_territory_land_2',
	3: 'sfx_territory_land_3',
} as const;

// Hunt Cascade multiplier config
export const HUNT_MULTIPLIER_CONFIG = {
	increment: 1,
	basegameCap: 50,
	freegameCap: 200,
	alphaDominationCap: 500,
};

// Territory thresholds for grid expansion
export const TERRITORY_THRESHOLDS = {
	3: '7x6' as GridSize,
	6: '8x7' as GridSize,
	10: '8x8' as GridSize,
};
