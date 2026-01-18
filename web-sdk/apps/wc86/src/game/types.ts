import { type SpinningReelSymbolState } from 'utils-slots';
import type config from './config';

// Symbol names for WC86 - Wolf Club 86
export type SymbolName = keyof typeof config.symbols;

export type RawSymbol = {
	name: SymbolName;
	multiplier?: number;
	scatter?: boolean;
	wild?: boolean;
	territory?: boolean;
};

export type BetMode = keyof typeof config.betModes;
export type GameType = 'basegame' | 'freegame' | 'alphaDomination';
export type GridSize = '6x5' | '7x6' | '8x7' | '8x8';
export type VolatilityMode = 'LONE_WOLF' | 'PACK' | 'ALPHA';

export const SYMBOL_STATES = [
	'static',
	'spin',
	'land',
	'win',
	'postWinStatic',
	'explosion',
] as const;

export type SymbolState = SpinningReelSymbolState | (typeof SYMBOL_STATES)[number];

export type Position = {
	reel: number;
	row: number;
	col?: number; // Alias for reel in grid context
};

// Grid size configuration (rows and cols)
export type GridSizeConfig = {
	rows: number;
	cols: number;
};

// Symbol ID type (all possible symbol names)
export type SymbolId =
	| 'BOSS_WOLF'
	| 'HUSTLER'
	| 'TECH_BRO'
	| 'DIAMOND_HANDS'
	| 'COCKTAIL'
	| 'VIP_CARD'
	| 'DISCO_BALL'
	| 'DICE'
	| 'ALPHA_WOLF'
	| 'HOWLING_WILD'
	| 'MOON_SCATTER'
	| 'TERRITORY';

// Game state for context
export type GameState = {
	board: (SymbolId | null)[][];
	gameType: GameType;
	currentGrid: GridSize;
	volatilityMode: VolatilityMode;
	huntMultiplier: number;
	cascadeCount: number;
	territoryLevel: number;
	freeSpinsRemaining: number;
	freeSpinsTotal: number;
};

// WC86 specific types
export type HuntMultiplierData = {
	huntMultiplier: number;
	cascadeCount: number;
	multCap: number;
};

export type PackSplitData = {
	alphaPosition: Position;
	splitCount: 2 | 3 | 4;
	affectedPositions: Position[];
	cumulativeMultiplier: number;
};

export type HowlChainData = {
	wildPositions: Array<Position & { multiplier: number }>;
	chainType: 'additive' | 'multiplicative';
	chainMultiplier: number;
};

export type TerritoryExpandData = {
	previousGrid: GridSize;
	newGrid: GridSize;
	territoryCount: number;
	newWaysCount: number;
};
