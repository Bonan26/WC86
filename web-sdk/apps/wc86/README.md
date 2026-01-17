# WC86 - Wolf Club 86 - Web SDK

## Context pour Claude (ELI)
Tu travailles sur le **Web Core** du jeu WC86 - Wolf Club 86 (state management, event handling, configuration). Theme: Nightclub retro 80s avec des loups. Ce README te donne tout le contexte necessaire.

## Architecture

### Stack Technique
- Svelte 5 (runes: $state, $derived, $effect)
- PixiJS 8 (via pixi-svelte)
- XState 5 (state machine)
- TypeScript strict

### Packages Stake SDK a utiliser
```typescript
// State & Config
import { stateBet, stateConfig } from 'state-shared';

// XState
import { createGameActor, createPrimaryMachines } from 'utils-xstate';

// Slots utilities
import { createReelForCascading, createEnhanceBoard } from 'utils-slots';

// Book events
import { createPlayBookUtils } from 'utils-book';

// Event emitter
import { createEventEmitter } from 'utils-event-emitter';

// Sound
import { createSound } from 'utils-sound';

// Layout
import { createLayout } from 'utils-layout';

// PixiJS components
import { App, Container, Sprite, Text } from 'pixi-svelte';
```

## Fichiers src/game/ a creer

### 1. types.ts
```typescript
export type SymbolName =
  | 'BOSS_WOLF' | 'HUSTLER' | 'TECH_BRO' | 'DIAMOND_HANDS'  // Premium wolves
  | 'COCKTAIL' | 'VIP_CARD' | 'DISCO_BALL' | 'DICE'         // Low (club items)
  | 'ALPHA_WOLF' | 'HOWLING_WILD' | 'MOON_SCATTER' | 'TERRITORY';  // Special

export type BetMode = 'base' | 'pack_hunt' | 'pack_hunt_plus' | 'alpha_domination';
export type GameType = 'basegame' | 'freegame' | 'alphaDomination';
export type GridConfig = '6x5' | '7x6' | '8x7' | '8x8';

export interface RawSymbol {
  name: SymbolName;
  multiplier?: number;
  wild?: boolean;
  scatter?: boolean;
  territory?: boolean;
}
```

### 2. typesBookEvent.ts
Voir `docs/INTEGRATION_CONTRACT.md` pour toutes les interfaces.

### 3. stateGame.svelte.ts
```typescript
export const stateGame = $state({
  board: createReelForCascading(6, 5),
  gameType: 'basegame' as GameType,
  currentGrid: '6x5' as GridConfig,
  volatilityMode: 'PACK',
  huntMultiplier: 1,
  cascadeCount: 0,
  territoryCollected: 0,
  scatterCounter: 0,
  freeSpinsRemaining: 0,
  totalWin: 0,
});
```

### 4. bookEventHandlerMap.ts (~400 lignes)
```typescript
export const bookEventHandlerMap = {
  reveal: async (data: RevealData, ctx: GameContext) => {
    stateGame.board = data.board;
    stateGame.gameType = data.gameType;
    stateGame.currentGrid = data.currentGrid;
    stateGame.huntMultiplier = data.huntMultiplier;
    await ctx.enhancedBoard.spin();
  },

  winInfo: async (data: WinInfoData, ctx: GameContext) => {
    for (const win of data.wins) {
      await ctx.eventEmitter.emit('symbolWin', win.positions);
    }
  },

  tumbleBoard: async (data: TumbleBoardData, ctx: GameContext) => {
    await ctx.eventEmitter.emit('symbolExplode', data.explodingPositions);
    await ctx.enhancedBoard.tumble(data.newSymbols);
  },

  updateHuntMultiplier: async (data: UpdateHuntMultiplierData, ctx: GameContext) => {
    stateGame.huntMultiplier = data.huntMultiplier;
    stateGame.cascadeCount = data.cascadeCount;
    await ctx.eventEmitter.emit('huntMultiplierUpdate', data);
  },

  packSplit: async (data: PackSplitData, ctx: GameContext) => {
    await ctx.eventEmitter.emit('packSplitAnimate', data);
  },

  howlChain: async (data: HowlChainData, ctx: GameContext) => {
    await ctx.eventEmitter.emit('howlChainAnimate', data);
  },

  territoryExpand: async (data: TerritoryExpandData, ctx: GameContext) => {
    stateGame.currentGrid = data.newGrid;
    await ctx.eventEmitter.emit('gridExpand', data);
  },

  // ... autres handlers
};
```

### 5. constants.ts (~300 lignes)
```typescript
export const SYMBOL_INFO_MAP = {
  BOSS_WOLF: {
    static: { type: 'sprite', src: 'symbolsStatic/boss_wolf.png' },
    spin: { type: 'spine', src: 'symbols/boss_wolf', anim: 'idle' },
    land: { type: 'spine', src: 'symbols/boss_wolf', anim: 'land' },
    win: { type: 'spine', src: 'symbols/boss_wolf', anim: 'win' },
    explosion: { type: 'spine', src: 'symbols/boss_wolf', anim: 'explosion' },
  },
  // ... 11 autres symboles
};

export const GRID_DIMENSIONS = {
  '6x5': { reels: 6, rows: 5, symbolWidth: 120, symbolHeight: 100 },
  '7x6': { reels: 7, rows: 6, symbolWidth: 105, symbolHeight: 90 },
  '8x7': { reels: 8, rows: 7, symbolWidth: 90, symbolHeight: 78 },
  '8x8': { reels: 8, rows: 8, symbolWidth: 90, symbolHeight: 70 },
};
```

### 6. config.ts
```typescript
export const gameConfig = {
  gameId: 'wc86',
  volatilityModes: ['LONE_WOLF', 'PACK', 'ALPHA'],
  defaultVolatility: 'PACK',
  betModes: {
    base: { cost: 1.0, label: 'Normal' },
    pack_hunt: { cost: 75.0, label: 'Buy Pack Hunt' },
    pack_hunt_plus: { cost: 150.0, label: 'Buy Pack Hunt+' },
    alpha_domination: { cost: 500.0, label: 'Alpha Domination' },
  },
  paytable: { ... },
};
```

## Emitter Events pour STEPH

Tu dois emettre ces events pour que STEPH anime:
```typescript
// Board
eventEmitter.emit('boardSpin');
eventEmitter.emit('boardReveal');
eventEmitter.emit('symbolWin', positions);
eventEmitter.emit('symbolExplode', positions);

// Hunt Multiplier
eventEmitter.emit('huntMultiplierShow');
eventEmitter.emit('huntMultiplierUpdate', { value, cascadeCount });
eventEmitter.emit('huntMultiplierHide');

// Features
eventEmitter.emit('packSplitAnimate', data);
eventEmitter.emit('howlChainAnimate', data);
eventEmitter.emit('gridExpand', data);

// Free Spins
eventEmitter.emit('freeSpinIntroShow', data);
eventEmitter.emit('freeSpinCounterUpdate', data);
eventEmitter.emit('freeSpinOutroShow', data);

// Alpha Domination
eventEmitter.emit('alphaDominationIntroShow', data);

// Big Wins
eventEmitter.emit('bigWinShow', { amount, level });
eventEmitter.emit('bigWinHide');
```

## Fichiers a creer

```
src/game/
├── actor.ts               # XState actor setup
├── assets.ts              # Asset manifest
├── bookEventHandlerMap.ts # Event handlers (~400 lignes)
├── config.ts              # Game config
├── constants.ts           # SYMBOL_INFO_MAP (~300 lignes)
├── context.ts             # Svelte context
├── eventEmitter.ts        # Event emitter
├── sound.ts               # Sound config
├── stateApp.ts            # App state
├── stateGame.svelte.ts    # Game state
├── stateLayout.ts         # Layout
├── stateXstate.ts         # State machine
├── types.ts               # Types
├── typesBookEvent.ts      # Book event types
├── typesEmitterEvent.ts   # Emitter types
├── utils.ts               # Helpers
└── winLevelMap.ts         # Win levels
```

## Commandes

```bash
# Dev
npm run dev

# Build
npm run build

# Storybook
npm run storybook

# Type check
npm run check
```