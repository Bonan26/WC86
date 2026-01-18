/**
 * WC86 - Wolf Club 86 - Core Types
 * Types de base pour le jeu
 */

// ============================================================================
// Symbol Types
// ============================================================================

/** Noms des symboles du jeu */
export type SymbolName =
  // Premium wolves (high pay)
  | 'BOSS_WOLF'
  | 'HUSTLER'
  | 'TECH_BRO'
  | 'DIAMOND_HANDS'
  // Low pay (club items)
  | 'COCKTAIL'
  | 'VIP_CARD'
  | 'DISCO_BALL'
  | 'DICE'
  // Special symbols
  | 'ALPHA_WOLF'
  | 'HOWLING_WILD'
  | 'MOON_SCATTER'
  | 'TERRITORY';

/** Symbole brut tel que recu du Math SDK */
export interface RawSymbol {
  name: SymbolName;
  multiplier?: number; // Pour HOWLING_WILD uniquement
  wild?: boolean; // true pour ALPHA_WOLF et HOWLING_WILD
  scatter?: boolean; // true pour MOON_SCATTER
  territory?: boolean; // true pour TERRITORY
}

// ============================================================================
// Game Configuration Types
// ============================================================================

/** Modes de mise disponibles */
export type BetMode = 'base' | 'pack_hunt' | 'pack_hunt_plus' | 'alpha_domination';

/** Types de jeu */
export type GameType = 'basegame' | 'freegame' | 'alphaDomination';

/** Configurations de grille (reels x rows) */
export type GridConfig = '6x5' | '7x6' | '8x7' | '8x8';

/** Modes de volatilite */
export type VolatilityMode = 'LONE_WOLF' | 'PACK' | 'ALPHA';

/** Niveaux de gain */
export type WinLevel = 'none' | 'big' | 'super' | 'mega' | 'epic' | 'max';

// ============================================================================
// Position Types
// ============================================================================

/** Position sur la grille */
export interface GridPosition {
  reel: number;
  row: number;
}

/** Position avec symbole */
export interface SymbolPosition extends GridPosition {
  symbol: RawSymbol;
}

// ============================================================================
// Feature Types
// ============================================================================

/** Type de chaine Howl */
export type HowlChainType = 'additive' | 'multiplicative';

/** Configuration d'un mode de mise */
export interface BetModeConfig {
  cost: number;
  label: string;
}

/** Dimensions d'une grille */
export interface GridDimensions {
  reels: number;
  rows: number;
  symbolWidth: number;
  symbolHeight: number;
}
