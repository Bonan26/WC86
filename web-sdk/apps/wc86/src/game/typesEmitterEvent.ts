/**
 * WC86 - Wolf Club 86 - Emitter Event Types
 * Types des events emis pour STEPH (animations)
 * Basé sur INTEGRATION_CONTRACT.md
 */

import type { GridPosition, WinLevel } from './types';
import type {
  PackSplitData,
  HowlChainData,
  TerritoryExpandData,
  AlphaDominationStartData,
} from './typesBookEvent';

// ============================================================================
// Board Events
// ============================================================================

export interface BoardSpinPayload {
  // Aucun payload requis
}

export interface BoardRevealPayload {
  // Aucun payload requis
}

export interface SymbolWinPayload {
  positions: GridPosition[];
}

export interface SymbolExplodePayload {
  positions: GridPosition[];
}

// ============================================================================
// Hunt Multiplier Events
// ============================================================================

export interface HuntMultiplierShowPayload {
  // Aucun payload requis
}

export interface HuntMultiplierUpdatePayload {
  value: number;
  cascadeCount: number;
}

export interface HuntMultiplierHidePayload {
  // Aucun payload requis
}

// ============================================================================
// Feature Events
// ============================================================================

export type PackSplitAnimatePayload = PackSplitData;

export type HowlChainAnimatePayload = HowlChainData;

export type GridExpandPayload = TerritoryExpandData;

// ============================================================================
// Free Spins Events
// ============================================================================

export interface FreeSpinIntroShowPayload {
  scatterCount: number;
  totalSpins: number;
}

export interface FreeSpinCounterUpdatePayload {
  remaining: number;
  total: number;
}

export interface FreeSpinOutroShowPayload {
  totalWin: number;
  spinCount: number;
  maxMultiplierReached: number;
  winLevel: WinLevel;
}

// ============================================================================
// Alpha Domination Events
// ============================================================================

export type AlphaDominationIntroShowPayload = AlphaDominationStartData;

// ============================================================================
// Big Win Events
// ============================================================================

export interface BigWinShowPayload {
  amount: number;
  level: Exclude<WinLevel, 'none'>;
}

export interface BigWinHidePayload {
  // Aucun payload requis
}

// ============================================================================
// Emitter Event Map
// ============================================================================

export interface EmitterEventMap {
  // Board
  boardSpin: BoardSpinPayload;
  boardReveal: BoardRevealPayload;
  symbolWin: SymbolWinPayload;
  symbolExplode: SymbolExplodePayload;

  // Hunt Multiplier
  huntMultiplierShow: HuntMultiplierShowPayload;
  huntMultiplierUpdate: HuntMultiplierUpdatePayload;
  huntMultiplierHide: HuntMultiplierHidePayload;

  // Features
  packSplitAnimate: PackSplitAnimatePayload;
  howlChainAnimate: HowlChainAnimatePayload;
  gridExpand: GridExpandPayload;

  // Free Spins
  freeSpinIntroShow: FreeSpinIntroShowPayload;
  freeSpinCounterUpdate: FreeSpinCounterUpdatePayload;
  freeSpinOutroShow: FreeSpinOutroShowPayload;

  // Alpha Domination
  alphaDominationIntroShow: AlphaDominationIntroShowPayload;

  // Big Wins
  bigWinShow: BigWinShowPayload;
  bigWinHide: BigWinHidePayload;
}

/** Noms des Emitter Events */
export type EmitterEventName = keyof EmitterEventMap;

/** Type helper pour obtenir le payload d'un event */
export type EmitterEventPayload<T extends EmitterEventName> = EmitterEventMap[T];
