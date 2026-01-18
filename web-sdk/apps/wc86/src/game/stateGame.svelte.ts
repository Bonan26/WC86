/**
 * WC86 - Wolf Club 86 - Game State
 * État reactif du jeu avec Svelte 5 runes
 */

import type { GameType, GridConfig, RawSymbol, VolatilityMode, WinLevel } from './types';

// ============================================================================
// State Interface
// ============================================================================

export interface GameState {
  // Board
  board: RawSymbol[][];
  gameType: GameType;
  currentGrid: GridConfig;

  // Volatility
  volatilityMode: VolatilityMode;

  // Hunt Multiplier
  huntMultiplier: number;
  cascadeCount: number;
  multCap: number;

  // Territory
  territoryCollected: number;

  // Scatter / Free Spins
  scatterCounter: number;
  freeSpinsRemaining: number;
  freeSpinsTotal: number;

  // Wins
  totalWin: number;
  spinWin: number;
  winLevel: WinLevel;

  // Alpha Domination
  isAlphaDomination: boolean;
  alphaDominationMultiplier: number;

  // UI State
  isSpinning: boolean;
  isCascading: boolean;
  isFeatureActive: boolean;
}

// ============================================================================
// Initial State
// ============================================================================

function createInitialBoard(): RawSymbol[][] {
  // Crée un board vide 6x5 (6 reels, 5 rows)
  return Array.from({ length: 6 }, () =>
    Array.from({ length: 5 }, () => ({ name: 'COCKTAIL' as const }))
  );
}

const initialState: GameState = {
  // Board
  board: createInitialBoard(),
  gameType: 'basegame',
  currentGrid: '6x5',

  // Volatility
  volatilityMode: 'PACK',

  // Hunt Multiplier
  huntMultiplier: 1,
  cascadeCount: 0,
  multCap: 100,

  // Territory
  territoryCollected: 0,

  // Scatter / Free Spins
  scatterCounter: 0,
  freeSpinsRemaining: 0,
  freeSpinsTotal: 0,

  // Wins
  totalWin: 0,
  spinWin: 0,
  winLevel: 'none',

  // Alpha Domination
  isAlphaDomination: false,
  alphaDominationMultiplier: 1,

  // UI State
  isSpinning: false,
  isCascading: false,
  isFeatureActive: false,
};

// ============================================================================
// Reactive State (Svelte 5 $state)
// ============================================================================

export const stateGame = $state<GameState>({ ...initialState });

// ============================================================================
// State Actions
// ============================================================================

/** Reset le state au state initial */
export function resetGameState(): void {
  Object.assign(stateGame, { ...initialState, board: createInitialBoard() });
}

/** Met a jour le board */
export function updateBoard(board: RawSymbol[][]): void {
  stateGame.board = board;
}

/** Met a jour le type de jeu */
export function setGameType(gameType: GameType): void {
  stateGame.gameType = gameType;
}

/** Met a jour la grille */
export function setCurrentGrid(grid: GridConfig): void {
  stateGame.currentGrid = grid;
}

/** Met a jour le Hunt Multiplier */
export function updateHuntMultiplier(multiplier: number, cascadeCount: number): void {
  stateGame.huntMultiplier = multiplier;
  stateGame.cascadeCount = cascadeCount;
}

/** Met a jour les free spins */
export function updateFreeSpins(remaining: number, total?: number): void {
  stateGame.freeSpinsRemaining = remaining;
  if (total !== undefined) {
    stateGame.freeSpinsTotal = total;
  }
}

/** Met a jour le win total */
export function updateTotalWin(amount: number): void {
  stateGame.totalWin = amount;
}

/** Met a jour le win du spin */
export function updateSpinWin(amount: number): void {
  stateGame.spinWin = amount;
}

/** Set le win level pour big win */
export function setWinLevel(level: WinLevel): void {
  stateGame.winLevel = level;
}

/** Active Alpha Domination */
export function startAlphaDomination(startingMultiplier: number, multCap: number): void {
  stateGame.isAlphaDomination = true;
  stateGame.alphaDominationMultiplier = startingMultiplier;
  stateGame.multCap = multCap;
  stateGame.gameType = 'alphaDomination';
}

/** Desactive Alpha Domination */
export function endAlphaDomination(): void {
  stateGame.isAlphaDomination = false;
  stateGame.alphaDominationMultiplier = 1;
  stateGame.multCap = 100;
}

/** Set spinning state */
export function setSpinning(isSpinning: boolean): void {
  stateGame.isSpinning = isSpinning;
}

/** Set cascading state */
export function setCascading(isCascading: boolean): void {
  stateGame.isCascading = isCascading;
}

/** Set feature active state */
export function setFeatureActive(isActive: boolean): void {
  stateGame.isFeatureActive = isActive;
}

/** Incremente le scatter counter */
export function incrementScatterCount(count: number): void {
  stateGame.scatterCounter += count;
}

/** Reset le scatter counter */
export function resetScatterCount(): void {
  stateGame.scatterCounter = 0;
}

/** Met a jour le territory collected */
export function updateTerritoryCollected(count: number): void {
  stateGame.territoryCollected = count;
}
