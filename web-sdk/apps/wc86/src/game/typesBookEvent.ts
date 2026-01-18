/**
 * WC86 - Wolf Club 86 - Book Event Types
 * Interfaces des events recus du Math SDK (DAN)
 */

import type {
  GameType,
  GridConfig,
  GridPosition,
  HowlChainType,
  RawSymbol,
  SymbolPosition,
  WinLevel,
} from './types';

// ============================================================================
// Book Event Data Interfaces
// ============================================================================

/** reveal - Affichage du board initial */
export interface RevealData {
  board: RawSymbol[][]; // [reel][row] format
  gameType: GameType;
  currentGrid: GridConfig;
  huntMultiplier: number;
  territoryCollected: number;
  paddingPositions: number[];
  anticipation: number[];
}

/** winInfo - Information sur les gains */
export interface WinInfoData {
  totalWin: number;
  wins: WinDetail[];
  huntMultiplier: number;
  chainMultiplier?: number;
}

/** Detail d'un gain individuel */
export interface WinDetail {
  symbol: string;
  count: number;
  positions: GridPosition[];
  payout: number;
  multiplier: number;
}

/** tumbleBoard - Cascade apres gain */
export interface TumbleBoardData {
  explodingPositions: GridPosition[];
  newSymbols: SymbolPosition[];
}

/** updateHuntMultiplier - Mise a jour du multiplicateur */
export interface UpdateHuntMultiplierData {
  huntMultiplier: number;
  cascadeCount: number;
  multCap: number;
}

/** packSplit - Alpha Wolf se duplique */
export interface PackSplitData {
  alphaPosition: GridPosition;
  splitCount: number; // 2, 3, ou 4
  affectedPositions: GridPosition[];
  cumulativeMultiplier: number; // x2, x3, x4
}

/** howlChain - Wilds adjacents */
export interface HowlChainData {
  wildPositions: Array<GridPosition & { multiplier: number }>;
  chainType: HowlChainType; // 2 wilds = add, 3+ = mult
  chainMultiplier: number;
}

/** territoryExpand - Expansion de grille */
export interface TerritoryExpandData {
  previousGrid: '6x5' | '7x6' | '8x7';
  newGrid: '7x6' | '8x7' | '8x8';
  territoryCount: number;
  newWaysCount: number;
}

/** alphaDominationStart - Debut super bonus */
export interface AlphaDominationStartData {
  startingMultiplier: number; // Min 5
  multCap: number; // 500
  guaranteedAlphaWolves: number;
}

/** freeSpinTrigger - Declenchement FS */
export interface FreeSpinTriggerData {
  scatterCount: number;
  scatterPositions: GridPosition[];
  totalSpins: number;
  isRetrigger: boolean;
}

/** freeSpinEnd - Fin des FS */
export interface FreeSpinEndData {
  totalWin: number;
  spinCount: number;
  maxMultiplierReached: number;
  winLevel: WinLevel;
}

/** setWin - Big win celebration */
export interface SetWinData {
  amount: number;
  winLevel: Exclude<WinLevel, 'none'>;
  multiplier: number;
}

// ============================================================================
// Book Event Union Type
// ============================================================================

/** Union de tous les Book Events WC86 */
export type WC86BookEvent =
  | { type: 'reveal'; data: RevealData }
  | { type: 'winInfo'; data: WinInfoData }
  | { type: 'tumbleBoard'; data: TumbleBoardData }
  | { type: 'updateHuntMultiplier'; data: UpdateHuntMultiplierData }
  | { type: 'packSplit'; data: PackSplitData }
  | { type: 'howlChain'; data: HowlChainData }
  | { type: 'territoryExpand'; data: TerritoryExpandData }
  | { type: 'alphaDominationStart'; data: AlphaDominationStartData }
  | { type: 'freeSpinTrigger'; data: FreeSpinTriggerData }
  | { type: 'freeSpinEnd'; data: FreeSpinEndData }
  | { type: 'setWin'; data: SetWinData };

/** Type literal des noms d'events */
export type BookEventType = WC86BookEvent['type'];

// ============================================================================
// Book Event Handler Types
// ============================================================================

/** Contexte passe aux handlers */
export interface GameContext {
  enhancedBoard: {
    spin: () => Promise<void>;
    tumble: (newSymbols: SymbolPosition[]) => Promise<void>;
    reveal: () => Promise<void>;
  };
  eventEmitter: {
    emit: (event: string, data?: unknown) => Promise<void>;
  };
}

/** Type d'un handler de Book Event */
export type BookEventHandler<T> = (data: T, ctx: GameContext) => Promise<void>;

/** Map des handlers par type d'event */
export type BookEventHandlerMap = {
  [K in BookEventType]: BookEventHandler<Extract<WC86BookEvent, { type: K }>['data']>;
};
