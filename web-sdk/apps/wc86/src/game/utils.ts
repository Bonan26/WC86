import _ from 'lodash';
import { stateBet } from 'state-shared';
import { createPlayBookUtils } from 'utils-book';
import { createGetEmptyPaddedBoard } from 'utils-slots';

import { SYMBOL_SIZE, REEL_PADDING, SYMBOL_INFO_MAP, BOARD_DIMENSIONS, GRID_CONFIGS } from './constants';
import { eventEmitter } from './eventEmitter';
import type { Bet, BookEventOfType } from './typesBookEvent';
import { bookEventHandlerMap } from './bookEventHandlerMap';
import type { RawSymbol, SymbolState, GridSize } from './types';

// General utils
export const { getEmptyBoard } = createGetEmptyPaddedBoard({ reelsDimensions: BOARD_DIMENSIONS });
export const { playBookEvent, playBookEvents } = createPlayBookUtils({ bookEventHandlerMap });

export const playBet = async (bet: Bet) => {
	stateBet.winBookEventAmount = 0;
	await playBookEvents(bet.state);
	eventEmitter.broadcast({ type: 'stopButtonEnable' });
};

// Resume bet helpers
const BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT = [
	'updateGlobalMult',
	'updateHuntMultiplier',
	'freeSpinTrigger',
	'updateFreeSpin',
	'setTotalWin',
	'territoryExpand',
];

export const convertToResumableBet = (betToResume: Bet) => {
	const resumingIndex = Number(betToResume.event);
	const bookEventsBeforeResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex < resumingIndex,
	);
	const bookEventsAfterResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex >= resumingIndex,
	);

	const bookEventToCreateSnapshot: BookEventOfType<'createBonusSnapshot'> = {
		index: 0,
		type: 'createBonusSnapshot',
		bookEvents: bookEventsBeforeResume.filter((bookEvent) =>
			BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT.includes(bookEvent.type),
		),
	};

	const stateToResume = [bookEventToCreateSnapshot, ...bookEventsAfterResume];

	return { ...betToResume, state: stateToResume };
};

// Symbol positioning utils
export const getSymbolX = (reelIndex: number) => SYMBOL_SIZE * (reelIndex + REEL_PADDING);
export const getSymbolY = (symbolIndexOfBoard: number) => (symbolIndexOfBoard + 0.5) * SYMBOL_SIZE;

// Get symbol info based on state
export const getSymbolInfo = ({
	rawSymbol,
	state,
}: {
	rawSymbol: RawSymbol;
	state: SymbolState;
}) => {
	const symbolInfo = SYMBOL_INFO_MAP[rawSymbol.name];
	if (symbolInfo && state in symbolInfo) {
		return symbolInfo[state as keyof typeof symbolInfo];
	}
	// Fallback to static if state not found
	return symbolInfo?.static || symbolInfo;
};

// Grid utils
export const getGridConfig = (gridSize: GridSize) => GRID_CONFIGS[gridSize];

export const getBoardDimensions = (gridSize: GridSize) => {
	const config = GRID_CONFIGS[gridSize];
	return { x: config.reels, y: config.rows };
};

export const getWaysCount = (gridSize: GridSize) => GRID_CONFIGS[gridSize].ways;

// Hunt multiplier utils
export const calculateHuntMultiplier = (cascadeCount: number, cap: number) => {
	return Math.min(1 + cascadeCount, cap);
};

// Pack split multiplier calculation
export const calculatePackSplitMultiplier = (splitCount: 2 | 3 | 4) => splitCount;

// Howl chain multiplier calculation
export const calculateHowlChainMultiplier = (
	wildCount: number,
	multipliers: number[],
	chainType: 'additive' | 'multiplicative'
) => {
	if (chainType === 'additive') {
		return multipliers.reduce((sum, m) => sum + m, 0);
	}
	return multipliers.reduce((product, m) => product * m, 1);
};
