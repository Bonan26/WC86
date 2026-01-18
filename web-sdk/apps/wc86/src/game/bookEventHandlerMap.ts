import { stateBet } from 'state-shared';
import { waitForTimeout } from 'utils-shared/wait';
import type { BookEventHandlerMap } from 'utils-book';

import { eventEmitter } from './eventEmitter';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import type { BookEvent, BookEventContext, BookEventOfType } from './typesBookEvent';
import { winLevelMap, winLevelDataMap, type WinLevelAlias } from './winLevelMap';

// Helper to get win level alias from multiplier
const getWinLevelAliasByMultiplier = (multiplier: number): WinLevelAlias => {
	const levels: WinLevelAlias[] = ['max', 'epic', 'mega', 'super', 'big', 'none'];
	for (const level of levels) {
		if (multiplier >= winLevelMap[level].threshold) {
			return level;
		}
	}
	return 'none';
};

export const bookEventHandlerMap: BookEventHandlerMap<BookEvent, BookEventContext> = {
	reveal: async (bookEvent: BookEventOfType<'reveal'>) => {
		const { data } = bookEvent;
		stateGame.gameType = data.gameType;
		stateGame.currentGrid = data.currentGrid;
		stateGame.huntMultiplier = data.huntMultiplier;
		stateGame.territoryCounter = data.territoryCollected;

		eventEmitter.broadcast({ type: 'boardSettle', board: data.board });
		eventEmitter.broadcast({ type: 'boardShow' });

		if (data.huntMultiplier > 1) {
			eventEmitter.broadcast({ type: 'huntMultiplierShow' });
			eventEmitter.broadcast({
				type: 'huntMultiplierUpdate',
				huntMultiplier: data.huntMultiplier,
				cascadeCount: 0,
				multCap: 50,
			});
		}

		await waitForTimeout(300);
	},

	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		const { wins, totalWin, huntMultiplier, chainMultiplier } = bookEvent.data;

		for (const win of wins) {
			eventEmitter.broadcast({
				type: 'boardWithAnimateSymbols',
				symbolPositions: win.positions,
			});
		}

		if (totalWin > 0) {
			stateBet.winBookEventAmount += totalWin;
			const winLevelAlias = getWinLevelAliasByMultiplier(
				stateBet.winBookEventAmount / stateBet.betAmount
			);
			const winLevelData = winLevelDataMap[winLevelAlias];

			eventEmitter.broadcast({ type: 'winShow' });
			eventEmitter.broadcast({
				type: 'winUpdate',
				amount: stateBet.winBookEventAmount,
				winLevelData,
			});
		}

		await waitForTimeout(500);
	},

	tumbleBoard: async (bookEvent: BookEventOfType<'tumbleBoard'>) => {
		const { explodingPositions, newSymbols } = bookEvent.data;

		// Explode winning symbols
		for (const pos of explodingPositions) {
			eventEmitter.broadcast({
				type: 'symbolExplode',
				position: pos,
			});
		}

		await waitForTimeout(300);

		// Cascade new symbols
		stateGame.cascadeCount++;
		eventEmitter.broadcast({ type: 'boardCascade', newSymbols });

		await waitForTimeout(400);
	},

	updateHuntMultiplier: async (bookEvent: BookEventOfType<'updateHuntMultiplier'>) => {
		const { data } = bookEvent;
		stateGame.huntMultiplier = data.huntMultiplier;
		stateGame.cascadeCount = data.cascadeCount;

		eventEmitter.broadcast({ type: 'huntMultiplierShow' });
		eventEmitter.broadcast({
			type: 'huntMultiplierUpdate',
			huntMultiplier: data.huntMultiplier,
			cascadeCount: data.cascadeCount,
			multCap: data.multCap,
		});

		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_multiplier_increase',
		});

		await waitForTimeout(300);
	},

	packSplit: async (bookEvent: BookEventOfType<'packSplit'>) => {
		eventEmitter.broadcast({
			type: 'packSplitAnimate',
			data: bookEvent.data,
		});

		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_pack_split',
		});

		await waitForTimeout(600);
	},

	howlChain: async (bookEvent: BookEventOfType<'howlChain'>) => {
		const { data } = bookEvent;
		eventEmitter.broadcast({
			type: 'howlChainAnimate',
			data,
		});

		const soundName = data.chainType === 'additive'
			? 'sfx_howl_chain_add'
			: 'sfx_howl_chain_multi';

		eventEmitter.broadcast({
			type: 'soundOnce',
			name: soundName,
		});

		await waitForTimeout(500);
	},

	territoryExpand: async (bookEvent: BookEventOfType<'territoryExpand'>) => {
		const { data } = bookEvent;
		stateGame.currentGrid = data.newGrid;
		stateGame.territoryCounter = data.territoryCount;

		eventEmitter.broadcast({
			type: 'gridExpand',
			data,
		});

		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_territory_expand',
		});

		await waitForTimeout(800);
	},

	alphaDominationStart: async (bookEvent: BookEventOfType<'alphaDominationStart'>) => {
		const { data } = bookEvent;
		stateGame.gameType = 'alphaDomination';
		stateGame.currentGrid = '8x8';
		stateGame.huntMultiplier = data.startingMultiplier;

		eventEmitter.broadcast({
			type: 'alphaDominationIntroShow',
			data,
		});

		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_alpha_domination_intro',
		});

		await waitForTimeout(2000);
	},

	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		const { data } = bookEvent;
		stateGame.gameType = 'freegame';
		stateGame.freeSpinsTotal = data.totalSpins;
		stateGame.freeSpinsRemaining = data.totalSpins;

		// Animate scatter positions
		for (const pos of data.scatterPositions) {
			eventEmitter.broadcast({
				type: 'symbolWin',
				position: pos,
			});
		}

		eventEmitter.broadcast({ type: 'freeSpinIntroShow' });
		eventEmitter.broadcast({
			type: 'freeSpinIntroUpdate',
			totalFreeSpins: data.totalSpins,
		});

		if (data.isRetrigger) {
			eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_freespin_retrigger',
			});
		} else {
			eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_freespin_trigger',
			});
		}

		await waitForTimeout(1500);
		eventEmitter.broadcast({ type: 'freeSpinIntroHide' });
		eventEmitter.broadcast({ type: 'transition' });
	},

	freeSpinEnd: async (bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		const { data } = bookEvent;
		stateGame.gameType = 'basegame';
		stateGame.huntMultiplier = 1;
		stateGame.cascadeCount = 0;

		const winLevelAlias = getWinLevelAliasByMultiplier(data.totalWin / stateBet.betAmount);
		const winLevelData = winLevelDataMap[winLevelAlias];

		eventEmitter.broadcast({ type: 'freeSpinOutroShow' });
		eventEmitter.broadcast({
			type: 'freeSpinOutroCountUp',
			amount: data.totalWin,
			winLevelData,
		});

		await waitForTimeout(winLevelData.presentDuration);
		eventEmitter.broadcast({ type: 'freeSpinOutroHide' });
		eventEmitter.broadcast({ type: 'transition' });

		// Reset hunt multiplier display
		eventEmitter.broadcast({ type: 'huntMultiplierHide' });
	},

	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		const { data } = bookEvent;
		const winLevelAlias = getWinLevelAliasByMultiplier(data.multiplier);
		const winLevelData = winLevelDataMap[winLevelAlias];

		eventEmitter.broadcast({ type: 'winShow' });
		eventEmitter.broadcast({
			type: 'winUpdate',
			amount: data.amount,
			winLevelData,
		});

		await waitForTimeout(winLevelData.presentDuration);
		eventEmitter.broadcast({ type: 'winHide' });
	},

	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
	},

	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		const { current, total } = bookEvent;
		stateGame.freeSpinsRemaining = total - current;
		stateGame.freeSpinsTotal = total;

		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current,
			total,
		});
	},

	updateGlobalMult: async (bookEvent: BookEventOfType<'updateGlobalMult'>) => {
		const { multiplier } = bookEvent;
		stateGame.huntMultiplier = multiplier;
		eventEmitter.broadcast({
			type: 'huntMultiplierUpdate',
			huntMultiplier: multiplier,
			cascadeCount: stateGame.cascadeCount,
			multCap: 500,
		});
	},

	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;
		// Process snapshot events to restore state
		for (const event of bookEvents) {
			if (event.type === 'updateGlobalMult') {
				stateGame.huntMultiplier = event.multiplier;
			}
			if (event.type === 'updateFreeSpin') {
				stateGame.freeSpinsRemaining = event.total - event.current;
				stateGame.freeSpinsTotal = event.total;
			}
			if (event.type === 'territoryExpand') {
				stateGame.currentGrid = event.data.newGrid;
				stateGame.territoryCounter = event.data.territoryCount;
			}
		}
	},
};
