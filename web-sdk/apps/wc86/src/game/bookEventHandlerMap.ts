/**
 * WC86 - Wolf Club 86 - Book Event Handler Map
 * Handlers pour les events recus du Math SDK (DAN)
 * Emet des Emitter Events pour les animations (STEPH)
 */

import {
  stateGame,
  updateBoard,
  setGameType,
  setCurrentGrid,
  updateHuntMultiplier,
  updateFreeSpins,
  updateTotalWin,
  updateSpinWin,
  setWinLevel,
  startAlphaDomination,
  endAlphaDomination,
  setSpinning,
  setCascading,
  setFeatureActive,
  updateTerritoryCollected,
} from './stateGame.svelte';

import type {
  BookEventHandlerMap,
  GameContext,
  RevealData,
  WinInfoData,
  TumbleBoardData,
  UpdateHuntMultiplierData,
  PackSplitData,
  HowlChainData,
  TerritoryExpandData,
  AlphaDominationStartData,
  FreeSpinTriggerData,
  FreeSpinEndData,
  SetWinData,
} from './typesBookEvent';

// ============================================================================
// Handler: reveal
// Affichage du board initial apres un spin
// ============================================================================

async function handleReveal(data: RevealData, ctx: GameContext): Promise<void> {
  // Update state
  updateBoard(data.board);
  setGameType(data.gameType);
  setCurrentGrid(data.currentGrid);
  updateHuntMultiplier(data.huntMultiplier, 0);
  updateTerritoryCollected(data.territoryCollected);

  // Emit board reveal
  await ctx.eventEmitter.emit('boardReveal');

  // Reveal via enhanced board
  await ctx.enhancedBoard.reveal();

  // Stop spinning state
  setSpinning(false);
}

// ============================================================================
// Handler: winInfo
// Information sur les gains d'un spin/cascade
// ============================================================================

async function handleWinInfo(data: WinInfoData, ctx: GameContext): Promise<void> {
  // Update state
  updateSpinWin(data.totalWin);
  updateTotalWin(stateGame.totalWin + data.totalWin);

  // Show hunt multiplier si > 1
  if (data.huntMultiplier > 1) {
    await ctx.eventEmitter.emit('huntMultiplierShow');
  }

  // Animate each win
  for (const win of data.wins) {
    await ctx.eventEmitter.emit('symbolWin', {
      positions: win.positions,
    });
  }
}

// ============================================================================
// Handler: tumbleBoard
// Cascade apres un gain - symboles explosent et nouveaux tombent
// ============================================================================

async function handleTumbleBoard(data: TumbleBoardData, ctx: GameContext): Promise<void> {
  // Set cascading state
  setCascading(true);

  // Emit explosion animation
  await ctx.eventEmitter.emit('symbolExplode', {
    positions: data.explodingPositions,
  });

  // Tumble via enhanced board (nouveaux symboles tombent)
  await ctx.enhancedBoard.tumble(data.newSymbols);

  // Update board state avec nouveaux symboles
  const newBoard = [...stateGame.board.map((reel) => [...reel])];
  for (const { reel, row, symbol } of data.newSymbols) {
    if (newBoard[reel] && newBoard[reel][row] !== undefined) {
      newBoard[reel][row] = symbol;
    }
  }
  updateBoard(newBoard);
}

// ============================================================================
// Handler: updateHuntMultiplier
// Mise a jour du multiplicateur de chasse apres cascade
// ============================================================================

async function handleUpdateHuntMultiplier(
  data: UpdateHuntMultiplierData,
  ctx: GameContext
): Promise<void> {
  // Update state
  updateHuntMultiplier(data.huntMultiplier, data.cascadeCount);
  stateGame.multCap = data.multCap;

  // Emit update animation
  await ctx.eventEmitter.emit('huntMultiplierUpdate', {
    value: data.huntMultiplier,
    cascadeCount: data.cascadeCount,
  });
}

// ============================================================================
// Handler: packSplit
// Alpha Wolf se duplique sur les positions adjacentes
// ============================================================================

async function handlePackSplit(data: PackSplitData, ctx: GameContext): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Emit pack split animation
  await ctx.eventEmitter.emit('packSplitAnimate', data);

  // Update board - les positions affectees deviennent des ALPHA_WOLF
  const newBoard = [...stateGame.board.map((reel) => [...reel])];
  for (const pos of data.affectedPositions) {
    if (newBoard[pos.reel] && newBoard[pos.reel][pos.row] !== undefined) {
      newBoard[pos.reel][pos.row] = {
        name: 'ALPHA_WOLF',
        wild: true,
      };
    }
  }
  updateBoard(newBoard);

  setFeatureActive(false);
}

// ============================================================================
// Handler: howlChain
// Wilds adjacents forment une chaine avec multiplicateur
// ============================================================================

async function handleHowlChain(data: HowlChainData, ctx: GameContext): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Emit howl chain animation
  await ctx.eventEmitter.emit('howlChainAnimate', data);

  // Update board - mettre a jour les multiplicateurs des wilds
  const newBoard = [...stateGame.board.map((reel) => [...reel])];
  for (const wildPos of data.wildPositions) {
    if (newBoard[wildPos.reel] && newBoard[wildPos.reel][wildPos.row] !== undefined) {
      const currentSymbol = newBoard[wildPos.reel][wildPos.row];
      newBoard[wildPos.reel][wildPos.row] = {
        ...currentSymbol,
        multiplier: wildPos.multiplier,
      };
    }
  }
  updateBoard(newBoard);

  setFeatureActive(false);
}

// ============================================================================
// Handler: territoryExpand
// Expansion de la grille quand assez de TERRITORY collectes
// ============================================================================

async function handleTerritoryExpand(data: TerritoryExpandData, ctx: GameContext): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Emit grid expand animation
  await ctx.eventEmitter.emit('gridExpand', data);

  // Update state
  setCurrentGrid(data.newGrid);
  updateTerritoryCollected(data.territoryCount);

  // Creer nouveau board avec la nouvelle taille
  const [reels, rows] = data.newGrid.split('x').map(Number);
  const newBoard: typeof stateGame.board = Array.from({ length: reels }, (_, reelIdx) =>
    Array.from({ length: rows }, (_, rowIdx) => {
      // Conserver les symboles existants si possible
      if (stateGame.board[reelIdx] && stateGame.board[reelIdx][rowIdx]) {
        return stateGame.board[reelIdx][rowIdx];
      }
      // Sinon placeholder (sera remplace par le prochain reveal)
      return { name: 'COCKTAIL' as const };
    })
  );
  updateBoard(newBoard);

  setFeatureActive(false);
}

// ============================================================================
// Handler: alphaDominationStart
// Debut du super bonus Alpha Domination
// ============================================================================

async function handleAlphaDominationStart(
  data: AlphaDominationStartData,
  ctx: GameContext
): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Update state
  startAlphaDomination(data.startingMultiplier, data.multCap);

  // Emit intro animation
  await ctx.eventEmitter.emit('alphaDominationIntroShow', data);

  setFeatureActive(false);
}

// ============================================================================
// Handler: freeSpinTrigger
// Declenchement des Free Spins
// ============================================================================

async function handleFreeSpinTrigger(data: FreeSpinTriggerData, ctx: GameContext): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Update free spins state
  if (data.isRetrigger) {
    const newRemaining = stateGame.freeSpinsRemaining + data.totalSpins;
    updateFreeSpins(newRemaining);

    // Emit counter update for retrigger
    await ctx.eventEmitter.emit('freeSpinCounterUpdate', {
      remaining: newRemaining,
      total: stateGame.freeSpinsTotal + data.totalSpins,
    });
  } else {
    updateFreeSpins(data.totalSpins, data.totalSpins);
    setGameType('freegame');

    // Emit intro animation
    await ctx.eventEmitter.emit('freeSpinIntroShow', {
      scatterCount: data.scatterCount,
      totalSpins: data.totalSpins,
    });
  }

  setFeatureActive(false);
}

// ============================================================================
// Handler: freeSpinEnd
// Fin des Free Spins
// ============================================================================

async function handleFreeSpinEnd(data: FreeSpinEndData, ctx: GameContext): Promise<void> {
  // Set feature active
  setFeatureActive(true);

  // Update state
  updateFreeSpins(0, 0);
  setWinLevel(data.winLevel);

  // Emit outro animation
  await ctx.eventEmitter.emit('freeSpinOutroShow', {
    totalWin: data.totalWin,
    spinCount: data.spinCount,
    maxMultiplierReached: data.maxMultiplierReached,
    winLevel: data.winLevel,
  });

  // Reset game state for base game
  setGameType('basegame');
  endAlphaDomination();
  updateHuntMultiplier(1, 0);

  setFeatureActive(false);
}

// ============================================================================
// Handler: setWin
// Big win celebration
// ============================================================================

async function handleSetWin(data: SetWinData, ctx: GameContext): Promise<void> {
  // Update state
  setWinLevel(data.winLevel);

  // Emit big win animation
  await ctx.eventEmitter.emit('bigWinShow', {
    amount: data.amount,
    level: data.winLevel,
  });

  // Wait for celebration to complete then hide
  await ctx.eventEmitter.emit('bigWinHide');

  // Reset win level
  setWinLevel('none');
}

// ============================================================================
// Export Handler Map
// ============================================================================

export const bookEventHandlerMap: BookEventHandlerMap = {
  reveal: handleReveal,
  winInfo: handleWinInfo,
  tumbleBoard: handleTumbleBoard,
  updateHuntMultiplier: handleUpdateHuntMultiplier,
  packSplit: handlePackSplit,
  howlChain: handleHowlChain,
  territoryExpand: handleTerritoryExpand,
  alphaDominationStart: handleAlphaDominationStart,
  freeSpinTrigger: handleFreeSpinTrigger,
  freeSpinEnd: handleFreeSpinEnd,
  setWin: handleSetWin,
};

// ============================================================================
// Book Event Processor
// ============================================================================

/**
 * Process un Book Event en appelant le handler correspondant
 */
export async function processBookEvent(
  event: { type: string; data: unknown },
  ctx: GameContext
): Promise<void> {
  const handler = bookEventHandlerMap[event.type as keyof BookEventHandlerMap];

  if (!handler) {
    console.warn(`[WC86] Unknown book event type: ${event.type}`);
    return;
  }

  try {
    await handler(event.data as never, ctx);
  } catch (error) {
    console.error(`[WC86] Error processing book event "${event.type}":`, error);
    throw error;
  }
}

/**
 * Process une sequence de Book Events
 */
export async function processBookEvents(
  events: Array<{ type: string; data: unknown }>,
  ctx: GameContext
): Promise<void> {
  for (const event of events) {
    await processBookEvent(event, ctx);
  }

  // Cacher le hunt multiplier a la fin si pas de cascades en cours
  if (!stateGame.isCascading && stateGame.huntMultiplier > 1) {
    await ctx.eventEmitter.emit('huntMultiplierHide');
  }

  // Reset cascading state
  setCascading(false);
}
