import type { RawSymbol, Position, GridSize, HuntMultiplierData, PackSplitData, HowlChainData, TerritoryExpandData } from './types';

// Book Event Types for WC86
export type BookEventType =
	| 'reveal'
	| 'winInfo'
	| 'tumbleBoard'
	| 'updateHuntMultiplier'
	| 'packSplit'
	| 'howlChain'
	| 'territoryExpand'
	| 'alphaDominationStart'
	| 'freeSpinTrigger'
	| 'freeSpinEnd'
	| 'setWin'
	| 'setTotalWin'
	| 'updateFreeSpin'
	| 'updateGlobalMult'
	| 'createBonusSnapshot';

// Reveal - Display initial board
export interface RevealData {
	board: RawSymbol[][];
	gameType: 'basegame' | 'freegame' | 'alphaDomination';
	currentGrid: GridSize;
	huntMultiplier: number;
	territoryCollected: number;
	paddingPositions: number[];
	anticipation: number[];
}

// Win Info - Information about wins
export interface WinInfoData {
	totalWin: number;
	wins: Array<{
		symbol: string;
		count: number;
		positions: Position[];
		payout: number;
		multiplier: number;
	}>;
	huntMultiplier: number;
	chainMultiplier?: number;
}

// Tumble Board - Cascade after win
export interface TumbleBoardData {
	explodingPositions: Position[];
	newSymbols: Array<Position & { symbol: RawSymbol }>;
}

// Free Spin Trigger
export interface FreeSpinTriggerData {
	scatterCount: number;
	scatterPositions: Position[];
	totalSpins: number;
	isRetrigger: boolean;
}

// Free Spin End
export interface FreeSpinEndData {
	totalWin: number;
	spinCount: number;
	maxMultiplierReached: number;
	winLevel: 'none' | 'big' | 'super' | 'mega' | 'epic' | 'max';
}

// Alpha Domination Start
export interface AlphaDominationStartData {
	startingMultiplier: number;
	multCap: number;
	guaranteedAlphaWolves: number;
}

// Set Win - Big win celebration
export interface SetWinData {
	amount: number;
	winLevel: 'big' | 'super' | 'mega' | 'epic' | 'max';
	multiplier: number;
}

// Book Event Union Type
export type BookEvent =
	| { index: number; type: 'reveal'; data: RevealData }
	| { index: number; type: 'winInfo'; data: WinInfoData }
	| { index: number; type: 'tumbleBoard'; data: TumbleBoardData }
	| { index: number; type: 'updateHuntMultiplier'; data: HuntMultiplierData }
	| { index: number; type: 'packSplit'; data: PackSplitData }
	| { index: number; type: 'howlChain'; data: HowlChainData }
	| { index: number; type: 'territoryExpand'; data: TerritoryExpandData }
	| { index: number; type: 'alphaDominationStart'; data: AlphaDominationStartData }
	| { index: number; type: 'freeSpinTrigger'; data: FreeSpinTriggerData }
	| { index: number; type: 'freeSpinEnd'; data: FreeSpinEndData }
	| { index: number; type: 'setWin'; data: SetWinData }
	| { index: number; type: 'setTotalWin'; amount: number }
	| { index: number; type: 'updateFreeSpin'; current: number; total: number }
	| { index: number; type: 'updateGlobalMult'; multiplier: number }
	| { index: number; type: 'createBonusSnapshot'; bookEvents: BookEvent[] };

export type BookEventOfType<T extends BookEventType> = Extract<BookEvent, { type: T }>;

export type Bet = {
	id: string;
	event: string;
	state: BookEvent[];
};
