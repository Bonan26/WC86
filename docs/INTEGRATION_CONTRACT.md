# CONTRAT D'INTEGRATION - WC86 (Wolf Club 86)

Ce document definit les interfaces entre les developpeurs.

## Format des Book Events (DAN → ELI)

```typescript
// Tous les events DOIVENT respecter ce format
interface BookEvent {
  type: string;           // Nom de l'event
  index: number;          // Index dans le book
  // ... data specifique
}

// Events WC86 specifiques:
type WC86BookEvent =
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
```

## Interfaces de donnees (Contrat DAN ↔ ELI)

```typescript
// reveal - Affichage du board initial
interface RevealData {
  board: RawSymbol[][];     // [reel][row] format
  gameType: 'basegame' | 'freegame' | 'alphaDomination';
  currentGrid: '6x5' | '7x6' | '8x7' | '8x8';
  huntMultiplier: number;
  territoryCollected: number;
  paddingPositions: number[];
  anticipation: number[];
}

// winInfo - Information sur les gains
interface WinInfoData {
  totalWin: number;
  wins: Array<{
    symbol: string;
    count: number;
    positions: Array<{reel: number; row: number}>;
    payout: number;
    multiplier: number;
  }>;
  huntMultiplier: number;
  chainMultiplier?: number;
}

// tumbleBoard - Cascade apres gain
interface TumbleBoardData {
  explodingPositions: Array<{reel: number; row: number}>;
  newSymbols: Array<{reel: number; row: number; symbol: RawSymbol}>;
}

// updateHuntMultiplier - Mise a jour du multiplicateur
interface UpdateHuntMultiplierData {
  huntMultiplier: number;
  cascadeCount: number;
  multCap: number;
}

// packSplit - Alpha Wolf se duplique
interface PackSplitData {
  alphaPosition: {reel: number; row: number};
  splitCount: number;        // 2, 3, ou 4
  affectedPositions: Array<{reel: number; row: number}>;
  cumulativeMultiplier: number;  // x2, x3, x4
}

// howlChain - Wilds adjacents
interface HowlChainData {
  wildPositions: Array<{reel: number; row: number; multiplier: number}>;
  chainType: 'additive' | 'multiplicative';  // 2 wilds = add, 3+ = mult
  chainMultiplier: number;
}

// territoryExpand - Expansion de grille
interface TerritoryExpandData {
  previousGrid: '6x5' | '7x6' | '8x7';
  newGrid: '7x6' | '8x7' | '8x8';
  territoryCount: number;
  newWaysCount: number;
}

// alphaDominationStart - Debut super bonus
interface AlphaDominationStartData {
  startingMultiplier: number;  // Min 5
  multCap: number;             // 500
  guaranteedAlphaWolves: number;
}

// freeSpinTrigger - Declenchement FS
interface FreeSpinTriggerData {
  scatterCount: number;
  scatterPositions: Array<{reel: number; row: number}>;
  totalSpins: number;
  isRetrigger: boolean;
}

// freeSpinEnd - Fin des FS
interface FreeSpinEndData {
  totalWin: number;
  spinCount: number;
  maxMultiplierReached: number;
  winLevel: 'none' | 'big' | 'super' | 'mega' | 'epic' | 'max';
}

// setWin - Big win celebration
interface SetWinData {
  amount: number;
  winLevel: 'big' | 'super' | 'mega' | 'epic' | 'max';
  multiplier: number;
}
```

## Format des Symboles (Contrat DAN ↔ ELI ↔ STEPH)

```typescript
interface RawSymbol {
  name: SymbolName;
  multiplier?: number;      // Pour HOWLING_WILD uniquement
  wild?: boolean;           // true pour ALPHA_WOLF et HOWLING_WILD
  scatter?: boolean;        // true pour MOON_SCATTER
  territory?: boolean;      // true pour TERRITORY
}

type SymbolName =
  | 'BOSS_WOLF' | 'HUSTLER' | 'TECH_BRO' | 'DIAMOND_HANDS'  // Premium
  | 'COCKTAIL' | 'VIP_CARD' | 'DISCO_BALL' | 'DICE'         // Low (club items)
  | 'ALPHA_WOLF' | 'HOWLING_WILD' | 'MOON_SCATTER' | 'TERRITORY';  // Special
```

## Emitter Events (Contrat ELI ↔ STEPH)

```typescript
// Events que ELI emet pour que STEPH anime
type EmitterEvent =
  // Board events
  | 'boardSpin'
  | 'boardReveal'
  | 'symbolWin'
  | 'symbolExplode'

  // Hunt Multiplier
  | 'huntMultiplierShow'
  | 'huntMultiplierUpdate'
  | 'huntMultiplierHide'

  // Pack Split
  | 'packSplitAnimate'

  // Howl Chain
  | 'howlChainAnimate'

  // Territory/Grid
  | 'gridExpand'

  // Free Spins
  | 'freeSpinIntroShow'
  | 'freeSpinCounterUpdate'
  | 'freeSpinOutroShow'

  // Alpha Domination
  | 'alphaDominationIntroShow'

  // Big Wins
  | 'bigWinShow'
  | 'bigWinHide';
```

## Nommage des Assets (Contrat ARIE ↔ STEPH)

```typescript
// Spine files - ARIE doit respecter ce nommage
const SPINE_PATHS = {
  // Symboles
  BOSS_WOLF: 'spines/symbols/boss_wolf/boss_wolf',
  HUSTLER: 'spines/symbols/hustler/hustler',
  TECH_BRO: 'spines/symbols/tech_bro/tech_bro',
  DIAMOND_HANDS: 'spines/symbols/diamond_hands/diamond_hands',
  COCKTAIL: 'spines/symbols/cocktail/cocktail',
  VIP_CARD: 'spines/symbols/vip_card/vip_card',
  DISCO_BALL: 'spines/symbols/disco_ball/disco_ball',
  DICE: 'spines/symbols/dice/dice',
  ALPHA_WOLF: 'spines/symbols/alpha_wolf/alpha_wolf',
  HOWLING_WILD: 'spines/symbols/howling_wild/howling_wild',
  MOON_SCATTER: 'spines/symbols/moon_scatter/moon_scatter',
  TERRITORY: 'spines/symbols/territory/territory',

  // Effets
  HUNT_MULTIPLIER: 'spines/effects/huntMultiplier/huntMultiplier',
  HOWL_CHAIN: 'spines/effects/howlChain/howlChain',
  PACK_SPLIT: 'spines/effects/packSplit/packSplit',
  TERRITORY_EXPAND: 'spines/effects/territoryExpand/territoryExpand',
  ALPHA_DOMINATION: 'spines/effects/alphaDomination/alphaDomination',
  BIGWIN: 'spines/effects/bigwin/bigwin',
  TRANSITION: 'spines/effects/transition/transition',
  ANTICIPATION: 'spines/effects/anticipation/anticipation',
};

// Animations requises par symbole
const REQUIRED_ANIMATIONS = {
  // Standard pour tous les symboles
  symbols: ['idle', 'land', 'win', 'explosion'],

  // Animations speciales
  ALPHA_WOLF: ['idle', 'land', 'win', 'explosion', 'split'],
  HOWLING_WILD: ['idle', 'land', 'win', 'explosion', 'howl'],
  TERRITORY: ['idle', 'land', 'win', 'explosion', 'glow'],

  // Effets
  effects: {
    huntMultiplier: ['idle', 'increase', 'maxed'],
    howlChain: ['chain_2', 'chain_3plus', 'connection'],
    packSplit: ['split', 'duplicate'],
    territoryExpand: ['expand_7x6', 'expand_8x7', 'expand_8x8'],
    alphaDomination: ['intro', 'idle', 'outro'],
    bigwin: ['big', 'super', 'mega', 'epic', 'max'],
    transition: ['base_to_fs', 'fs_to_base'],
    anticipation: ['intro', 'loop', 'outro'],
  }
};

// Audio sprites - ARIE doit respecter ce nommage dans sounds.json
const AUDIO_SPRITES = {
  // BGM
  bgm_main: { start: 0, duration: 120000, loop: true },
  bgm_freespin: { start: 120000, duration: 90000, loop: true },
  bgm_alpha_domination: { start: 210000, duration: 60000, loop: true },

  // SFX
  sfx_spin_start: { start: 270000, duration: 500 },
  sfx_reel_stop: { start: 270500, duration: 200 },
  sfx_cascade_explosion: { start: 270700, duration: 400 },
  sfx_multiplier_increase: { start: 271100, duration: 300 },
  sfx_pack_split: { start: 271400, duration: 600 },
  sfx_howl_chain_add: { start: 272000, duration: 500 },
  sfx_howl_chain_multi: { start: 272500, duration: 700 },
  sfx_territory_expand: { start: 273200, duration: 800 },
  sfx_scatter_land: { start: 274000, duration: 400 },
  sfx_freespin_trigger: { start: 274400, duration: 1500 },
  sfx_alpha_domination_intro: { start: 275900, duration: 2000 },
  // ... etc (60 total)
};
```

## Responsabilites

### DAN (Math-SDK)
- Generer tous les book events avec le format ci-dessus
- S'assurer que les indices de position sont corrects (reel, row)
- Valider que le RTP est dans les tolerances

### ELI (Web Core)
- Implementer tous les handlers pour chaque event type
- Emettre les emitter events pour STEPH
- Gerer l'etat du jeu (stateGame)

### STEPH (Components)
- Ecouter les emitter events de ELI
- Implementer les animations correspondantes
- Utiliser les paths d'assets definis par ARIE

### ARIE (Assets)
- Respecter EXACTEMENT les nommages ci-dessus
- Fournir toutes les animations listees dans REQUIRED_ANIMATIONS
- Generer le sounds.json avec les bons timings
