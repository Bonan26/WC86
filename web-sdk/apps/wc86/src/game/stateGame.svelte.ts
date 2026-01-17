import _ from 'lodash';
import type { Tween } from 'svelte/motion';

import { stateBet } from 'state-shared';
import { createEnhanceBoard, createReelForCascading } from 'utils-slots';
import { createGetWinLevelDataByWinLevelAlias } from 'utils-shared/winLevel';

import type { GameType, RawSymbol, SymbolState, GridSize, VolatilityMode } from './types';
import { stateLayoutDerived } from './stateLayout';
import { winLevelMap } from './winLevelMap';
import { eventEmitter } from './eventEmitter';
import {
	SYMBOL_SIZE,
	BOARD_SIZES,
	INITIAL_BOARD,
	BOARD_DIMENSIONS,
	SPIN_OPTIONS_DEFAULT,
	SPIN_OPTIONS_FAST,
	INITIAL_SYMBOL_STATE,
	SCATTER_LAND_SOUND_MAP,
	TERRITORY_LAND_SOUND_MAP,
	GRID_CONFIGS,
} from './constants';

// Track scatter and territory landings for sounds
let scatterLandCount = 0;
let territoryLandCount = 0;

const onSymbolLand = ({ rawSymbol }: { rawSymbol: RawSymbol }) => {
	// Moon Scatter landing
	if (rawSymbol.name === 'MOON_SCATTER') {
		scatterLandCount++;
		eventEmitter.broadcast({ type: 'soundScatterCounterIncrease' });
		const soundIndex = Math.min(scatterLandCount, 6) as 1 | 2 | 3 | 4 | 5 | 6;
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: SCATTER_LAND_SOUND_MAP[soundIndex],
		});
	}

	// Territory symbol landing
	if (rawSymbol.name === 'TERRITORY') {
		territoryLandCount++;
		const soundIndex = Math.min(territoryLandCount, 3) as 1 | 2 | 3;
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: TERRITORY_LAND_SOUND_MAP[soundIndex],
		});
	}

	// Alpha Wolf landing
	if (rawSymbol.name === 'ALPHA_WOLF') {
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_alpha_wolf_land',
		});
	}

	// Howling Wild landing
	if (rawSymbol.name === 'HOWLING_WILD') {
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_howling_wild_land',
		});
	}
};

// Create board with cascading reels
const board = _.range(BOARD_DIMENSIONS.x).map((reelIndex) => {
	const reel = createReelForCascading({
		reelIndex,
		symbolHeight: SYMBOL_SIZE,
		initialSymbols: INITIAL_BOARD[reelIndex],
		initialSymbolState: INITIAL_SYMBOL_STATE,
		onReelStopping: () => {
			eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_reel_stop',
				forcePlay: !stateBet.isTurbo,
			});
		},
		onSymbolLand,
	});

	reel.reelState.spinOptions = () =>
		reel.reelState.spinType === 'fast' ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT;

	return reel;
});

export type Reel = (typeof board)[number];
export type ReelSymbol = Reel['reelState']['symbols'][number];

export type MultiplierSymbol = {
	initX: number;
	initY: number;
	symbolX: Tween<number>;
	symbolY: Tween<number>;
	rawSymbol: RawSymbol;
	symbolState: SymbolState;
	oncomplete: () => void;
};

// Main game state
export const stateGame = $state({
	board,
	gameType: 'basegame' as GameType,
	currentGrid: '6x5' as GridSize,
	volatilityMode: 'PACK' as VolatilityMode,
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
	territoryCounter: 0,
	huntMultiplier: 1,
	cascadeCount: 0,
	freeSpinsRemaining: 0,
	freeSpinsTotal: 0,
});

// Board layout calculations
const boardLayout = () => {
	const gridConfig = GRID_CONFIGS[stateGame.currentGrid];
	const currentBoardSizes = {
		width: SYMBOL_SIZE * gridConfig.reels,
		height: SYMBOL_SIZE * gridConfig.rows,
	};

	return {
		x: stateLayoutDerived.mainLayout().width * 0.5,
		y: stateLayoutDerived.mainLayout().height * 0.5,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: currentBoardSizes.width / 2, y: currentBoardSizes.height / 2 },
		...currentBoardSizes,
	};
};

const boardRaw = () =>
	board.map((reel) => reel.reelState.symbols.map((reelSymbol) => reelSymbol.rawSymbol));

const scatterLandIndex = () => {
	if (stateGame.scatterCounter > 6) return 6;
	if (stateGame.scatterCounter < 1) return 1;
	return stateGame.scatterCounter as 1 | 2 | 3 | 4 | 5 | 6;
};

const resetCounters = () => {
	scatterLandCount = 0;
	territoryLandCount = 0;
	stateGame.scatterCounter = 0;
	stateGame.territoryCounter = 0;
};

const { enhanceBoard } = createEnhanceBoard();
const enhancedBoard = enhanceBoard({ board: stateGame.board });

export const { getWinLevelDataByWinLevelAlias } = createGetWinLevelDataByWinLevelAlias({
	winLevelMap,
});

export const stateGameDerived = {
	onSymbolLand,
	boardLayout,
	boardRaw,
	scatterLandIndex,
	resetCounters,
	enhancedBoard,
	getWinLevelDataByWinLevelAlias,
};
