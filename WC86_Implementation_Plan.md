# WC86 - Wolf Club 86 - PLAN D'IMPLÉMENTATION EXHAUSTIF

**Version:** 3.0 - Équipe & Intégration
**Date:** Janvier 2026
**Jeu:** WC86 (Wolf Club 86) - Slot haute volatilité 6x5→8x8
**Theme:** Nightclub retro 80s avec des loups

---

# TABLE DES MATIÈRES

0. [Organisation Équipe & GitHub](#partie-0-organisation-équipe--github)
1. [Vue d'ensemble](#partie-1-vue-densemble)
2. [SDK Stake à utiliser](#partie-2-sdk-stake-à-utiliser)
3. [Math-SDK Implementation](#partie-3-math-sdk-implementation)
4. [Web-SDK Implementation](#partie-4-web-sdk-implementation)
5. [Assets à créer](#partie-5-assets-à-créer-100)
6. [Intégration & Tests](#partie-6-intégration--tests)
7. [Structure Dossiers & README Context](#partie-7-structure-dossiers--readme-context)

---

# PARTIE 0: ORGANISATION ÉQUIPE & GITHUB

## 0.1 Répartition du travail

| Dev | Rôle | Scope | Branch |
|-----|------|-------|--------|
| **DAN** | Math Engine | Math-SDK complet (Python + Rust optimization) | `feature/math-sdk` |
| **ELI** | Web Core | Web-SDK game/ + state + event handlers | `feature/web-core` |
| **STEPH** | Web Components | Web-SDK components/ + animations Svelte | `feature/web-components` |
| **ARIE** | Assets | Tous les assets (Nano Banana API) | `feature/assets` |

## 0.2 Détail des responsabilités

### DAN - Math Engine Lead
**Fichiers à créer:**
```
math-sdk/games/wc86/
├── __init__.py
├── game_config.py          # Config, paytable, symbols, bet modes
├── gamestate.py            # GameState, run_spin, run_freespin
├── game_override.py        # Symbol functions, special mechanics
├── game_executables.py     # Ways evaluation, Howl Chain
├── game_calculations.py    # Math utilities
├── game_events.py          # Custom events emission
├── game_optimization.py    # Rust optimization setup
├── run.py                  # Main entry point
└── reels/                  # 11 CSV files
```

**Dépendances Stake SDK:**
- `src/config/` - Config, BetMode, Distribution
- `src/calculations/` - Symbol, Board, Ways, Tumble
- `src/state/` - GeneralGameState, Book
- `optimization_program/` - Rust Pig Farm algorithm

**Livrables:**
1. Simulations fonctionnelles (500k+ spins)
2. RTP validé: 96.2%-96.8% selon mode
3. JSON configs pour RGS
4. Stat sheets avec hit rates

---

### ELI - Web Core Lead
**Fichiers à créer:**
```
web-sdk/apps/wc86/src/game/
├── actor.ts                # XState actor setup
├── assets.ts               # Asset manifest
├── bookEventHandlerMap.ts  # Event → Animation mapping (~400 lignes)
├── config.ts               # Game config mirror
├── constants.ts            # SYMBOL_INFO_MAP, dimensions (~300 lignes)
├── context.ts              # Svelte context providers
├── eventEmitter.ts         # Custom emitter events
├── sound.ts                # Sound sprite config
├── stateApp.ts             # App-level state
├── stateGame.svelte.ts     # Game state (board, multipliers, etc.)
├── stateLayout.ts          # Layout calculations
├── stateXstate.ts          # State machine definitions
├── types.ts                # TypeScript types
├── typesBookEvent.ts       # Book event types (18 events)
├── typesEmitterEvent.ts    # Emitter event types
├── utils.ts                # Helper functions
└── winLevelMap.ts          # Win level thresholds
```

**Fichiers config racine:**
```
web-sdk/apps/wc86/
├── package.json
├── svelte.config.js
├── tsconfig.json
├── vite.config.ts
├── lingui.config.ts
└── src/app.html
```

**Dépendances Stake SDK packages:**
- `utils-xstate` - createGameActor, createPrimaryMachines
- `utils-slots` - createReelForCascading, createEnhanceBoard
- `utils-book` - createPlayBookUtils
- `state-shared` - stateBet, stateConfig
- `pixi-svelte` - App, Container, Sprite

**Livrables:**
1. State machine fonctionnelle
2. Event handlers pour tous les 18 events
3. Integration avec STEPH pour components
4. Integration avec DAN pour book events format

---

### STEPH - Web Components Lead
**Fichiers à créer:**
```
web-sdk/apps/wc86/src/components/
├── core/                   # Adapté de ways
│   ├── Game.svelte
│   ├── Board.svelte
│   ├── BoardBase.svelte
│   ├── BoardContainer.svelte
│   ├── BoardFrame.svelte
│   ├── BoardMask.svelte
│   ├── Symbol.svelte
│   ├── SymbolSpine.svelte
│   ├── SymbolSprite.svelte
│   ├── TumbleBoard.svelte
│   ├── TumbleBoardBase.svelte
│   ├── TumbleSymbol.svelte
│   ├── Win.svelte
│   ├── WinAnimation.svelte
│   ├── WinCoins.svelte
│   ├── FreeSpinIntro.svelte
│   ├── FreeSpinOutro.svelte
│   ├── FreeSpinCounter.svelte
│   ├── Transition.svelte
│   ├── TransitionAnimation.svelte
│   ├── Background.svelte
│   └── LoadingScreen.svelte
├── custom/                 # Nouveaux pour WC86
│   ├── HuntMultiplier.svelte
│   ├── HowlChainEffect.svelte
│   ├── PackSplitAnimation.svelte
│   ├── TerritoryExpand.svelte
│   ├── GridExpansion.svelte
│   ├── AlphaDominationIntro.svelte
│   └── VolatilitySelector.svelte
├── routes/
│   ├── +layout.svelte
│   ├── +page.svelte
│   └── +page.ts
├── stories/
│   ├── base_books.stories.ts
│   ├── bonus_books.stories.ts
│   ├── components.stories.ts
│   └── data/
└── i18n/
    ├── en.json
    ├── fr.json
    └── messages.ts
```

**.storybook/ config:**
```
web-sdk/apps/wc86/.storybook/
├── main.ts
└── preview.ts
```

**Dépendances Stake SDK packages:**
- `components-pixi` - Spine, AnimatedSprite
- `components-layout` - MainContainer
- `components-ui-pixi` - UI, ButtonBuyBonus
- `components-ui-html` - Modals

**Livrables:**
1. 29 composants core adaptés
2. 7 composants custom fonctionnels
3. Storybook avec tous les stories
4. Animations smooth 60fps

---

### ARIE - Assets Lead (Nano Banana API)
**Structure à créer:**
```
web-sdk/apps/wc86/static/assets/
├── audio/
│   ├── sounds.mp3          # Sprite audio principal
│   └── sounds.json         # Config des 60 sprites audio
├── fonts/
│   ├── alphaFont/          # Police principale
│   ├── goldFont/           # Police wins
│   └── cryptoFont/         # Police crypto
├── spines/
│   ├── symbols/            # 12 symboles animés
│   │   ├── boss_wolf/
│   │   ├── hustler/
│   │   ├── tech_bro/
│   │   ├── diamond_hands/
│   │   ├── cocktail/
│   │   ├── vip_card/
│   │   ├── disco_ball/
│   │   ├── dice/
│   │   ├── alpha_wolf/
│   │   ├── howling_wild/
│   │   ├── moon_scatter/
│   │   └── territory/
│   └── effects/            # 8 effets animés
│       ├── huntMultiplier/
│       ├── howlChain/
│       ├── packSplit/
│       ├── territoryExpand/
│       ├── alphaDomination/
│       ├── bigwin/
│       ├── transition/
│       └── anticipation/
└── sprites/
    ├── symbolsStatic/      # 12 PNG symboles
    ├── reelsFrame/         # Cadre grille dynamique
    ├── freeSpins/
    ├── progressBar/
    ├── pressToContinueText/
    └── uiAssets/
```

**Livrables:**
1. 60 sprites audio (sounds.json)
2. 3 fonts complètes
3. 20 dossiers Spine avec animations
4. 6 dossiers sprites PNG

---

## 0.3 CONTRAT D'INTÉGRATION

### Format des Book Events (DAN → ELI)

```typescript
// Tous les events DOIVENT respecter ce format
interface BookEvent {
  type: string;           // Nom de l'event
  data: Record<string, any>;
}

// Events WC86 spécifiques:
type AlphaWolvesBookEvent =
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

### Interfaces de données (Contrat DAN ↔ ELI)

```typescript
// reveal - Affichage du board initial
interface RevealData {
  board: RawSymbol[][];     // [reel][row] format
  gameType: 'basegame' | 'freegame' | 'alphaDomination';
  currentGrid: '6x5' | '7x6' | '8x7' | '8x8';
  huntMultiplier: number;
  territoryCollected: number;
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

// tumbleBoard - Cascade après gain
interface TumbleBoardData {
  explodingPositions: Array<{reel: number; row: number}>;
  newSymbols: Array<{reel: number; row: number; symbol: RawSymbol}>;
}

// updateHuntMultiplier - Mise à jour du multiplicateur
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

// alphaDominationStart - Début super bonus
interface AlphaDominationStartData {
  startingMultiplier: number;  // Min 5
  multCap: number;             // 500
  guaranteedAlphaWolves: number;
}

// freeSpinTrigger - Déclenchement FS
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

### Format des Symboles (Contrat DAN ↔ ELI ↔ STEPH)

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

### Emitter Events (Contrat ELI ↔ STEPH)

```typescript
// Events que ELI émet pour que STEPH anime
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

### Nommage des Assets (Contrat ARIE ↔ STEPH)

```typescript
// Spine files - ARIE doit respecter ce nommage
const SPINE_PATHS = {
  // Symboles
  BOSS_WOLF: 'spines/symbols/boss_wolf/boss_wolf',
  HUSTLER: 'spines/symbols/hustler/hustler',
  // ... etc

  // Effets
  HUNT_MULTIPLIER: 'spines/effects/huntMultiplier/huntMultiplier',
  HOWL_CHAIN: 'spines/effects/howlChain/howlChain',
  // ... etc
};

// Animations requises par symbole
const REQUIRED_ANIMATIONS = {
  symbols: ['idle', 'land', 'win', 'explosion'],
  ALPHA_WOLF: ['idle', 'land', 'win', 'explosion', 'split'],
  HOWLING_WILD: ['idle', 'land', 'win', 'explosion', 'howl'],
  TERRITORY: ['idle', 'land', 'win', 'explosion', 'glow'],
  effects: {
    huntMultiplier: ['idle', 'increase', 'maxed'],
    howlChain: ['chain_2', 'chain_3plus', 'connection'],
    packSplit: ['split', 'duplicate'],
    territoryExpand: ['expand_7x6', 'expand_8x7', 'expand_8x8'],
    alphaDomination: ['intro', 'idle', 'outro'],
    bigwin: ['big', 'super', 'mega', 'epic', 'max'],
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

---

## 0.4 Workflow GitHub

### Branches
```
main
├── develop                      # Integration branch
├── feature/math-sdk            # DAN
├── feature/web-core            # ELI
├── feature/web-components      # STEPH
└── feature/assets              # ARIE
```

### Règles de merge
1. Chaque dev travaille sur sa branch
2. PR vers `develop` quand feature complète
3. Review obligatoire par 1 autre dev
4. CI doit passer (lint, types, tests)
5. Merge `develop` → `main` quand milestone atteint

### Milestones
| Milestone | Critères | Responsables |
|-----------|----------|--------------|
| M1: Math Core | Simulations 100k fonctionnelles | DAN |
| M2: Web Skeleton | App démarre, state machine OK | ELI |
| M3: Basic Spin | Spin basique avec symboles statiques | ELI + STEPH |
| M4: Assets V1 | Symboles statiques + 1 animation | ARIE |
| M5: Cascade | Hunt Cascade fonctionnel | DAN + ELI + STEPH |
| M6: Features | Pack Split, Howl Chain, Territory | ALL |
| M7: Free Spins | Pack Hunt complet | ALL |
| M8: Polish | Alpha Domination + audio + polish | ALL |
| M9: QA | Tests complets, RTP validé | ALL |

---

## 0.5 Communication quotidienne

### Standup format (async sur Discord/Slack)
```
**[NOM] - [DATE]**
✅ Done: ...
🔄 Today: ...
🚫 Blockers: ...
```

### Channels
- `#alpha-wolves-general` - Discussion générale
- `#alpha-wolves-integration` - Questions sur les contrats
- `#alpha-wolves-pr` - Notifications PR

---

# PARTIE 1: VUE D'ENSEMBLE

## Caractéristiques du jeu WC86

| Propriété | Valeur |
|-----------|--------|
| **Type** | Slot Ways-to-Win avec Cascade |
| **Grille** | 6x5 → 7x6 → 8x7 → 8x8 (dynamique) |
| **Ways** | 7,776 → 46,656 → 117,649 → 262,144 |
| **RTP** | 96.2% - 96.8% (selon mode) |
| **Volatilité** | Extrême (3 modes) |
| **Max Win** | 10,000x / 25,000x / 50,000x |

## Modes de volatilité

| Mode | RTP | Max Win | Hit Freq | FS Mult Cap |
|------|-----|---------|----------|-------------|
| LONE_WOLF 🐺 | 96.8% | 10,000x | ~35% | x50 |
| PACK 🐺🐺 | 96.5% | 25,000x | ~25% | x200 |
| ALPHA 🐺🐺🐺 | 96.2% | 50,000x | ~15% | x500 |

## Features uniques

1. **Hunt Cascade** - Tumble avec multiplicateur persistant (+1 par cascade)
2. **Pack Split** - Alpha Wolf dédouble symboles à gauche (x2, x3, x4 cumulatif)
3. **Territory Expand** - 3/6/10 Territory = grille 7x6/8x7/8x8
4. **Howl Chain** - Wilds adjacents: 2=additif, 3+=multiplicatif
5. **Pack Hunt** - Free Spins (10-20 FS, mult persistant)
6. **Alpha Domination** - Super Bonus (8x8 fixe, mult min x5)

## Bet Modes

| Mode | Coût | Type | Description |
|------|------|------|-------------|
| base | 1.0x | Standard | Jeu normal |
| pack_hunt | 75x | Buy Bonus | 10 FS garantis |
| pack_hunt_plus | 150x | Buy Bonus | 15 FS, grille 7x6, mult x3 |
| alpha_domination | 500x | Buy Bonus | 20 FS, 8x8 fixe, mult x5 |

---

# PARTIE 2: SDK STAKE À UTILISER

## 1.1 MATH-SDK - Modules réutilisables

### src/config/ - Configuration

| Fichier | Classe/Fonction | À utiliser pour |
|---------|-----------------|-----------------|
| `config.py` | `Config` | Classe parent de GameConfig |
| `betmode.py` | `BetMode` | Définir les 4 bet modes |
| `distributions.py` | `Distribution` | Définir les distributions (wincap, freegame, basegame) |
| `optimization_paramaters.py` | `OptimizationParameters` | Paramètres d'optimisation RTP |
| `output_filenames.py` | `OutputFiles` | Gestion des chemins de sortie |
| `paths.py` | Constantes | `PATH_TO_GAMES`, `OPTIMIZATION_PATH` |
| `constants.py` | Mappings | `ANTEMAPPING`, `ISBUYBONUSMAPPING` |

### src/calculations/ - Calculs de gains

| Fichier | Classe | À utiliser pour |
|---------|--------|-----------------|
| `symbol.py` | `Symbol`, `SymbolDefinition`, `SymbolStorage` | Gestion des 12 symboles |
| `board.py` | `Board` | Génération plateau 6x5→8x8 |
| `ways.py` | `Ways` | **Calcul des gains ways** |
| `tumble.py` | `Tumble` | **Hunt Cascade** (explosion + refill) |
| `statistics.py` | `get_random_outcome()` | Tirage multiplicateurs Howling Wild |

### src/state/ - Gestion d'état

| Fichier | Classe | À utiliser pour |
|---------|--------|-----------------|
| `state.py` | `GeneralGameState` | État global, cycle de vie |
| `state_conditions.py` | `Conditions` | Vérifications (in_criteria, is_wincap) |
| `books.py` | `Book` | Stockage événements simulation |
| `run_sims.py` | `create_books()` | Orchestration multi-thread |

### src/events/ - Événements

| Fichier | Fonctions | À utiliser pour |
|---------|-----------|-----------------|
| `events.py` | `reveal_event()` | Affichage plateau |
| | `win_info_event()` | Détails des gains |
| | `set_win_event()` | Mise à jour ticker |
| | `fs_trigger_event()` | Déclenchement FS |
| | `update_freespin_event()` | Update compteur FS |
| | `freespin_end_event()` | Fin FS |
| | `tumble_board_event()` | Cascade board |
| | `update_global_mult_event()` | Multiplicateur global |
| `event_constants.py` | `EventConstants` | Enum des types |

### src/wins/ - Gestion gains

| Fichier | Classe/Fonction | À utiliser pour |
|---------|-----------------|-----------------|
| `win_manager.py` | `WinManager` | Tracking gains (spin, base, free) |
| `multiplier_strategy.py` | `apply_mult()` | Stratégies mult (global, symbol, combined) |

### src/executables/ - Actions

| Fichier | Classe | À utiliser pour |
|---------|--------|-----------------|
| `executables.py` | `Executables` | Actions communes (tumble, wincap, FS) |

### src/write_data/ - Sortie

| Fichier | Fonction | À utiliser pour |
|---------|----------|-----------------|
| `write_data.py` | `make_lookup_tables()` | Générer CSV lookup |
| | `write_json()` | Sérialiser books |
| `write_configs.py` | `generate_configs()` | Générer config.json |
| `force.py` | `IdentityCondition` | Recherche simulations |

---

## 1.2 OPTIMIZATION_PROGRAM - Programme Rust

### Fichiers à utiliser

| Fichier | Rôle |
|---------|------|
| `optimization_config.py` | Classes Python pour config |
| `run_script.py` | `OptimizationExecution` - Lance Rust |
| `src/main.rs` | Algorithme "Pig Farm" |
| `src/setup.rs` | Lecture setup.toml |
| `src/exes.rs` | Structures JSON |
| `Cargo.toml` | Dépendances Rust |

### Classes Python pour config

```python
from optimization_program.optimization_config import (
    ConstructScaling,      # Conditions de scaling RTP
    ConstructParameters,   # Params d'optimisation
    ConstructConditions,   # Critères (RTP, HR, avg_win)
    ConstructFenceBias,    # Bias pour distributions
    verify_optimization_input  # Validation
)
```

### Flux d'optimisation

```
1. GameConfig.opt_params = {...}  # Définir paramètres
2. OptimizationSetup(config)      # Valider
3. generate_configs(gamestate)    # Écrire math_config.json
4. OptimizationExecution().run_all_modes(config, modes, threads)
   └─ Écrit setup.toml
   └─ Lance: cargo run --release
   └─ Rust lit lookup_tables/*.csv
   └─ Rust optimise distributions
   └─ Rust écrit optimization_files/
5. generate_configs(gamestate)    # Régénérer avec résultats
```

---

## 1.3 UTILS/ - Utilitaires Python

| Dossier | Module | À utiliser pour |
|---------|--------|-----------------|
| `game_analytics/` | `create_stat_sheet()` | Générer rapports XLSX/JSON |
| `analysis/` | `calculate_rtp()`, `make_win_distribution()` | Analyse statistique |
| `merge_luts/` | `run()` | Fusionner tables lookup |
| `rgs_verification.py` | `WinStatistics` | Vérification format RGS |

---

## 1.4 WEB-SDK - Packages réutilisables

### Packages CORE (obligatoires)

| Package | Import | À utiliser pour |
|---------|--------|-----------------|
| `pixi-svelte` | `App`, `Sprite`, `Text`, `Container`, `SpineProvider`, `SpineTrack`, `BitmapText`, `ParticleEmitter` | Rendu PixiJS |
| `state-shared` | `stateBet`, `stateConfig`, `stateModal`, `stateSound`, `stateUi`, `stateI18n` | États globaux |
| `utils-xstate` | `createGameActor`, `createPrimaryMachines`, `createIntermediateMachines`, `createXstateUtils` | Machine d'état XState |
| `utils-slots` | `createReelForCascading`, `createEnhanceBoard`, `createEnhanceBoardSpin`, `createEnhanceBoardPreSpin` | Logique slots/tumble |
| `utils-book` | `createPlayBookUtils`, `createMultiBookUtils`, `checkIsMultipleRevealEvents`, `recordBookEvent` | Gestion book events |
| `utils-event-emitter` | `createEventEmitter`, context | Event system typé |
| `utils-sound` | `createSound` | Audio Howler.js |
| `utils-layout` | `createLayout` | Layout responsif |
| `utils-shared` | `waitForTimeout`, `sequence`, `createInterruptible` | Utilitaires |
| `constants-shared` | `API_AMOUNT_MULTIPLIER`, `BOOK_AMOUNT_MULTIPLIER` | Constantes |
| `rgs-requests` | `requestBet`, `requestAuthenticate`, `requestEndRound` | Requêtes RGS |

### Packages COMPONENTS (obligatoires)

| Package | Composants | À utiliser pour |
|---------|------------|-----------------|
| `components-pixi` | `EnablePixiExtension`, `FadeContainer`, `LoadingProgress`, `WinCountUpProvider`, `ResponsiveBitmapText`, `Button`, `Amount` | Composants Pixi |
| `components-ui-pixi` | `UI`, `UiGameName`, `ButtonAutoSpin`, `ButtonBet`, `ButtonBuyBonus`, `ButtonTurbo`, `LabelBalance`, `LabelWin`, `LabelFreeSpinCounter` | UI complète |
| `components-ui-html` | `Modals`, `GameVersion`, `GlobalStyle`, modales (AutoSpin, BetMenu, BuyBonus, PayTable, Settings) | Modales HTML |
| `components-layout` | `MainContainer`, `OnPressFullScreen` | Layout principal |
| `components-shared` | `Authenticate`, `LoaderStakeEngine`, `EnableHotkey`, `EnableSpaceHold`, `LoadI18n`, `BoardContext` | Auth, loaders, hotkeys |

### Packages CONFIG

| Package | Fichier | À utiliser pour |
|---------|---------|-----------------|
| `config-ts` | `base.json` | tsconfig.json |
| `config-vite` | `index.js` | vite.config.ts |
| `config-svelte` | `index.js` | svelte.config.js |
| `config-storybook` | `index.ts` | .storybook/main.ts |
| `config-lingui` | `index.ts` | lingui.config.ts |
| `eslint-config-custom` | `.eslintrc.js` | .eslintrc.cjs |

---

# PARTIE 2: MATH-SDK IMPLEMENTATION

## 2.1 Structure des fichiers

```
math-sdk/games/wc86/
├── __init__.py                    # Export module
├── game_config.py                 # ~350 lignes
├── gamestate.py                   # ~200 lignes
├── game_override.py               # ~150 lignes
├── game_executables.py            # ~100 lignes
├── game_calculations.py           # ~50 lignes
├── game_events.py                 # ~120 lignes
├── game_optimization.py           # ~200 lignes
├── run.py                         # ~100 lignes
├── README.md
└── reels/
    ├── BR_LONE_WOLF.csv          # Base Reel - Mode LONE_WOLF
    ├── BR_PACK.csv               # Base Reel - Mode PACK
    ├── BR_ALPHA.csv              # Base Reel - Mode ALPHA
    ├── FR_LONE_WOLF.csv          # Free Reel - Mode LONE_WOLF
    ├── FR_PACK.csv               # Free Reel - Mode PACK
    ├── FR_ALPHA.csv              # Free Reel - Mode ALPHA
    ├── FR_WINCAP_LONE.csv        # Free Reel Wincap - LONE_WOLF
    ├── FR_WINCAP_PACK.csv        # Free Reel Wincap - PACK
    ├── FR_WINCAP_ALPHA.csv       # Free Reel Wincap - ALPHA
    ├── AD_BASE.csv               # Alpha Domination Base
    └── AD_WINCAP.csv             # Alpha Domination Wincap
```

## 2.2 game_config.py - Configuration complète

```python
"""WC86 Game Configuration"""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode

class GameConfig(Config):
    """Configuration complète pour WC86."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

        # === IDENTIFICATION ===
        self.game_id = "wc86"
        self.provider_number = 0
        self.provider_name = "stake_originals"
        self.game_name = "WC86"
        self.working_name = "Alpha Wolves - Crypto Wolf Pack"
        self.win_type = "ways"
        self.construct_paths()

        # === VOLATILITY MODES ===
        self.volatility_modes = {
            "LONE_WOLF": {"rtp": 0.968, "wincap": 10000, "fs_mult_cap": 50},
            "PACK": {"rtp": 0.965, "wincap": 25000, "fs_mult_cap": 200},
            "ALPHA": {"rtp": 0.962, "wincap": 50000, "fs_mult_cap": 500}
        }
        self.active_volatility = "PACK"

        # === GRID CONFIGURATIONS ===
        self.base_num_reels = 6
        self.base_num_rows = [5] * 6
        self.num_reels = 6
        self.num_rows = [5] * 6

        self.grid_configs = {
            "6x5": {"reels": 6, "rows": [5]*6, "ways": 7776},
            "7x6": {"reels": 7, "rows": [6]*7, "ways": 46656},
            "8x7": {"reels": 8, "rows": [7]*8, "ways": 117649},
            "8x8": {"reels": 8, "rows": [8]*8, "ways": 262144}
        }
        self.current_grid = "6x5"

        # === SYMBOLS (12 total) ===
        self.premium_symbols = ["BOSS_WOLF", "HUSTLER", "TECH_BRO", "DIAMOND_HANDS"]
        self.low_symbols = ["COCKTAIL", "VIP_CARD", "DISCO_BALL", "DICE"]
        self.wild_symbols = ["ALPHA_WOLF", "HOWLING_WILD"]
        self.scatter_symbols = ["MOON_SCATTER"]
        self.territory_symbols = ["TERRITORY"]

        # === PAYTABLE ===
        self.paytable = {
            # BOSS_WOLF (Highest Premium)
            (6, "BOSS_WOLF"): 50, (5, "BOSS_WOLF"): 25,
            (4, "BOSS_WOLF"): 10, (3, "BOSS_WOLF"): 5,
            # HUSTLER
            (6, "HUSTLER"): 30, (5, "HUSTLER"): 15,
            (4, "HUSTLER"): 6, (3, "HUSTLER"): 3,
            # TECH_BRO
            (6, "TECH_BRO"): 20, (5, "TECH_BRO"): 10,
            (4, "TECH_BRO"): 4, (3, "TECH_BRO"): 2,
            # DIAMOND_HANDS
            (6, "DIAMOND_HANDS"): 15, (5, "DIAMOND_HANDS"): 7.5,
            (4, "DIAMOND_HANDS"): 3, (3, "DIAMOND_HANDS"): 1.5,
            # COCKTAIL (Martini neon 80s)
            (6, "COCKTAIL"): 5, (5, "COCKTAIL"): 2.5,
            (4, "COCKTAIL"): 1, (3, "COCKTAIL"): 0.5,
            # VIP_CARD (Carte membre doree)
            (6, "VIP_CARD"): 4, (5, "VIP_CARD"): 2,
            (4, "VIP_CARD"): 0.8, (3, "VIP_CARD"): 0.4,
            # DISCO_BALL (Boule disco)
            (6, "DISCO_BALL"): 3, (5, "DISCO_BALL"): 1.5,
            (4, "DISCO_BALL"): 0.6, (3, "DISCO_BALL"): 0.3,
            # DICE (Des lumineux neon)
            (6, "DICE"): 2, (5, "DICE"): 1,
            (4, "DICE"): 0.4, (3, "DICE"): 0.2,
        }

        # === SPECIAL SYMBOLS ===
        self.special_symbols = {
            "wild": ["ALPHA_WOLF", "HOWLING_WILD"],
            "scatter": ["MOON_SCATTER"],
            "territory": ["TERRITORY"],
            "multiplier": ["HOWLING_WILD"]
        }

        # === HOWLING WILD MULTIPLIERS ===
        self.howling_wild_mult_values = {
            "basegame": {2: 40, 3: 30, 5: 20, 10: 10},
            "freegame": {2: 20, 3: 25, 5: 30, 10: 20, 15: 5}
        }

        # === ALPHA WOLF SPLIT PROBABILITIES ===
        self.alpha_split_probs = {2: 60, 3: 30, 4: 10}

        # === FREE SPIN TRIGGERS ===
        self.freespin_triggers = {
            "basegame": {3: 10, 4: 12, 5: 15, 6: 20},
            "freegame": {2: 3, 3: 5, 4: 8, 5: 10, 6: 15}
        }
        self.anticipation_triggers = {"basegame": 2, "freegame": 1}

        # === HUNT CASCADE CONFIG ===
        self.tumble_mult_increment = 1
        self.tumble_mult_cap = {"basegame": 50, "freegame": 200}
        self.tumble_mult_persistent_in_fs = True

        # === TERRITORY THRESHOLDS ===
        self.territory_thresholds = {3: "7x6", 6: "8x7", 10: "8x8"}

        # === ALPHA DOMINATION CONFIG ===
        self.alpha_domination_config = {
            "grid": "8x8",
            "min_multiplier": 5,
            "mult_cap": 500
        }

        # === FEATURE BUY COSTS ===
        self.feature_buy_costs = {
            "pack_hunt": 75,
            "pack_hunt_plus": 150,
            "alpha_domination": 500
        }

        self.include_padding = True
        self._load_reels()
        self._setup_bet_modes()

    def _load_reels(self):
        """Load all reel strips."""
        reels_map = {
            "BR_LONE": "BR_LONE_WOLF.csv",
            "BR_PACK": "BR_PACK.csv",
            "BR_ALPHA": "BR_ALPHA.csv",
            "FR_LONE": "FR_LONE_WOLF.csv",
            "FR_PACK": "FR_PACK.csv",
            "FR_ALPHA": "FR_ALPHA.csv",
            "FRCAP_LONE": "FR_WINCAP_LONE.csv",
            "FRCAP_PACK": "FR_WINCAP_PACK.csv",
            "FRCAP_ALPHA": "FR_WINCAP_ALPHA.csv",
            "AD_BASE": "AD_BASE.csv",
            "AD_WCAP": "AD_WINCAP.csv"
        }
        self.reels = {}
        for key, filename in reels_map.items():
            self.reels[key] = self.read_reels_csv(
                os.path.join(self.reels_path, filename)
            )

    def _setup_bet_modes(self):
        """Configure all bet modes."""
        vol = self.volatility_modes[self.active_volatility]

        self.bet_modes = [
            # BASE MODE
            BetMode(
                name="base",
                cost=1.0,
                rtp=vol["rtp"],
                max_win=vol["wincap"],
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=vol["wincap"],
                        conditions={
                            "reel_weights": {
                                "basegame": {"BR_PACK": 1},
                                "freegame": {"FR_PACK": 1, "FRCAP_PACK": 5}
                            },
                            "force_wincap": True,
                            "force_freegame": True,
                            "scatter_triggers": {3: 50, 4: 30, 5: 15, 6: 5},
                            "howling_mult_values": self.howling_wild_mult_values["freegame"],
                        }
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.08,
                        conditions={
                            "reel_weights": {
                                "basegame": {"BR_PACK": 1},
                                "freegame": {"FR_PACK": 1}
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {3: 70, 4: 20, 5: 8, 6: 2},
                        }
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.35,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {"basegame": {"BR_PACK": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        }
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.569,
                        conditions={
                            "reel_weights": {"basegame": {"BR_PACK": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        }
                    ),
                ]
            ),
            # PACK HUNT (75x)
            BetMode(
                name="pack_hunt",
                cost=75.0,
                rtp=vol["rtp"],
                max_win=vol["wincap"],
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                "basegame": {"BR_PACK": 1},
                                "freegame": {"FR_PACK": 1, "FRCAP_PACK": 3}
                            },
                            "force_freegame": True,
                            "scatter_triggers": {3: 100},
                        }
                    )
                ]
            ),
            # PACK HUNT PLUS (150x)
            BetMode(
                name="pack_hunt_plus",
                cost=150.0,
                rtp=vol["rtp"],
                max_win=vol["wincap"],
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame_enhanced",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                "basegame": {"BR_PACK": 1},
                                "freegame": {"FR_PACK": 1, "FRCAP_PACK": 5}
                            },
                            "force_freegame": True,
                            "scatter_triggers": {4: 100},
                            "starting_multiplier": 3,
                            "starting_grid": "7x6",
                        }
                    )
                ]
            ),
            # ALPHA DOMINATION (500x)
            BetMode(
                name="alpha_domination",
                cost=500.0,
                rtp=vol["rtp"],
                max_win=vol["wincap"],
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="alpha_domination",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                "basegame": {"AD_BASE": 1},
                                "freegame": {"AD_BASE": 1, "AD_WCAP": 8}
                            },
                            "force_freegame": True,
                            "fixed_grid": "8x8",
                            "starting_multiplier": 5,
                            "mult_cap": 500,
                            "scatter_triggers": {3: 100},
                        }
                    )
                ]
            ),
        ]

    def set_volatility_mode(self, mode: str):
        """Switch volatility mode."""
        if mode not in self.volatility_modes:
            raise ValueError(f"Invalid mode: {mode}")
        self.active_volatility = mode
        vol = self.volatility_modes[mode]
        self.rtp = vol["rtp"]
        self.wincap = vol["wincap"]
        self.tumble_mult_cap["freegame"] = vol["fs_mult_cap"]
        self._setup_bet_modes()

    def expand_grid(self, new_grid: str):
        """Expand grid configuration."""
        if new_grid not in self.grid_configs:
            raise ValueError(f"Invalid grid: {new_grid}")
        cfg = self.grid_configs[new_grid]
        self.num_reels = cfg["reels"]
        self.num_rows = cfg["rows"]
        self.current_grid = new_grid

    def reset_grid(self):
        """Reset to base 6x5 grid."""
        self.num_reels = self.base_num_reels
        self.num_rows = self.base_num_rows.copy()
        self.current_grid = "6x5"
```

## 2.3 gamestate.py - Boucle de jeu

```python
"""WC86 GameState - Core game loop."""

from game_override import GameStateOverride
from game_events import (
    territory_expand_event,
    pack_split_event,
    howl_chain_event,
    alpha_domination_start_event,
    update_hunt_multiplier_event
)

class GameState(GameStateOverride):
    """Game loop with Hunt Cascade, Pack Split, Territory Expand."""

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        """Main base game spin."""
        self.reset_seed(sim)
        self.repeat = True

        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=True)

            # Initialize Hunt Cascade
            self.hunt_multiplier = 1
            self.cascade_count = 0

            # Process initial board
            self.process_alpha_wolf_split()
            self.evaluate_ways_board_with_wilds()
            self.emit_hunt_cascade_events()

            # Hunt Cascade loop
            while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
                self.cascade_count += 1
                self.update_hunt_multiplier()
                self.tumble_game_board()
                self.process_alpha_wolf_split()
                self.evaluate_ways_board_with_wilds()
                self.emit_hunt_cascade_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            # Check Territory Expand
            if self.check_territory_condition():
                self.process_territory_expand()

            # Check Free Spins
            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        """Pack Hunt free spins with persistent multiplier."""
        self.reset_fs_spin()

        # Check Alpha Domination mode
        if self.in_criteria("alpha_domination"):
            self.run_alpha_domination()
            return

        # Standard Pack Hunt
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board(emit_event=True)

            self.process_alpha_wolf_split()
            self.evaluate_ways_board_with_wilds()
            self.emit_hunt_cascade_events()

            # Cascade loop (multiplier persists!)
            while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
                self.cascade_count += 1
                self.update_hunt_multiplier()
                self.tumble_game_board()
                self.process_alpha_wolf_split()
                self.evaluate_ways_board_with_wilds()
                self.emit_hunt_cascade_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            # Territory Expand during FS
            if self.check_territory_condition():
                self.process_territory_expand()

            # Retrigger check
            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()

    def run_alpha_domination(self) -> None:
        """Alpha Domination super bonus - 8x8 fixed, min x5."""
        alpha_domination_start_event(self)

        # Force 8x8 grid
        self.config.expand_grid("8x8")
        conditions = self.get_current_distribution_conditions()
        self.hunt_multiplier = conditions.get("starting_multiplier", 5)

        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board(emit_event=True)

            self.process_alpha_wolf_split()
            self.evaluate_ways_board_with_wilds()
            self.emit_hunt_cascade_events()

            while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
                self.cascade_count += 1
                self.update_hunt_multiplier()
                self.tumble_game_board()
                self.process_alpha_wolf_split()
                self.evaluate_ways_board_with_wilds()
                self.emit_hunt_cascade_events()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.config.reset_grid()
        self.end_freespin()

    def process_alpha_wolf_split(self) -> None:
        """Alpha Wolf splits symbols to the left."""
        positions = self.get_symbol_positions("ALPHA_WOLF")
        if not positions.get("ALPHA_WOLF"):
            return

        for pos in positions["ALPHA_WOLF"]:
            reel, row = pos["reel"], pos["row"]
            if reel > 0:
                left_symbol = self.board[reel - 1][row]
                split_count = self.get_alpha_split_count()
                pack_split_event(self, reel, row, left_symbol.name, split_count)
                self.apply_pack_split(reel, row, left_symbol.name, split_count)

    def process_territory_expand(self) -> None:
        """Expand grid based on Territory count."""
        count = self.count_symbols_on_board("TERRITORY")
        for threshold, grid in sorted(self.config.territory_thresholds.items()):
            if count >= threshold and self.config.current_grid != grid:
                self.config.expand_grid(grid)
                territory_expand_event(self, grid)
                break
```

## 2.4 game_events.py - Événements custom

```python
"""WC86 Custom Events."""

from src.events.events import *

def territory_expand_event(gamestate, new_grid: str):
    """Grid expansion event."""
    cfg = gamestate.config.grid_configs[new_grid]
    event = {
        "index": len(gamestate.book.events),
        "type": "territoryExpand",
        "newGrid": new_grid,
        "newReels": cfg["reels"],
        "newRows": cfg["rows"],
        "waysCount": cfg["ways"],
        "territoriesCollected": gamestate.territory_collected
    }
    gamestate.book.add_event(event)

def pack_split_event(gamestate, reel: int, row: int, symbol: str, mult: int):
    """Alpha Wolf pack split event."""
    event = {
        "index": len(gamestate.book.events),
        "type": "packSplit",
        "alphaPosition": {"reel": reel, "row": row + 1},
        "targetSymbol": symbol,
        "splitMultiplier": mult
    }
    gamestate.book.add_event(event)

def howl_chain_event(gamestate, wilds: list, mult: int):
    """Howling Wild chain event."""
    positions = [{"reel": w["reel"], "row": w["row"] + 1} for w in wilds]
    event = {
        "index": len(gamestate.book.events),
        "type": "howlChain",
        "wildPositions": positions,
        "wildCount": len(wilds),
        "chainType": "additive" if len(wilds) == 2 else "multiplicative",
        "chainMultiplier": mult
    }
    gamestate.book.add_event(event)

def alpha_domination_start_event(gamestate):
    """Alpha Domination super bonus start."""
    event = {
        "index": len(gamestate.book.events),
        "type": "alphaDominationStart",
        "fixedGrid": "8x8",
        "startingMultiplier": gamestate.hunt_multiplier,
        "multCap": gamestate.config.alpha_domination_config["mult_cap"]
    }
    gamestate.book.add_event(event)

def update_hunt_multiplier_event(gamestate):
    """Hunt multiplier update event."""
    event = {
        "index": len(gamestate.book.events),
        "type": "updateHuntMultiplier",
        "huntMultiplier": gamestate.hunt_multiplier,
        "cascadeCount": gamestate.cascade_count,
        "multCap": gamestate.config.tumble_mult_cap.get(gamestate.gametype, 50)
    }
    gamestate.book.add_event(event)

def volatility_mode_event(gamestate, mode: str):
    """Volatility mode change event."""
    vol = gamestate.config.volatility_modes[mode]
    event = {
        "index": len(gamestate.book.events),
        "type": "volatilityModeChange",
        "mode": mode,
        "rtp": vol["rtp"],
        "maxWin": vol["wincap"]
    }
    gamestate.book.add_event(event)
```

## 2.5 run.py - Point d'entrée

```python
"""WC86 - Main simulation entry point."""

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # === CONFIGURATION ===
    num_threads = 12
    rust_threads = 24
    batching_size = 100000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(5e5),           # 500k simulations
        "pack_hunt": int(2e5),      # 200k
        "pack_hunt_plus": int(1e5), # 100k
        "alpha_domination": int(5e4) # 50k
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": True,
        "run_analysis": True,
        "run_format_checks": True,
    }

    target_modes = ["base", "pack_hunt", "pack_hunt_plus", "alpha_domination"]

    # === VOLATILITY MODE ===
    volatility_mode = "PACK"  # LONE_WOLF, PACK, or ALPHA

    # === INITIALIZATION ===
    config = GameConfig()
    config.set_volatility_mode(volatility_mode)
    gamestate = GameState(config)

    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        optimization_setup = OptimizationSetup(config)

    # === RUN SIMULATIONS ===
    if run_conditions["run_sims"]:
        print(f"\n=== WC86 Simulations ===")
        print(f"Volatility: {volatility_mode}")
        print(f"RTP: {config.rtp} | Max Win: {config.wincap}x\n")

        create_books(
            gamestate, config, num_sim_args,
            batching_size, num_threads, compression, profiling
        )

    generate_configs(gamestate)

    # === RUN RUST OPTIMIZATION ===
    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    # === RUN ANALYSIS ===
    if run_conditions["run_analysis"]:
        custom_keys = [
            {"symbol": "scatter"},
            {"symbol": "territory"},
            {"feature": "pack_split"},
            {"feature": "howl_chain"},
        ]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    # === RUN VERIFICATION ===
    if run_conditions["run_format_checks"]:
        execute_all_tests(config)

    print(f"\n=== WC86 Complete ===")
```

---

# PARTIE 3: WEB-SDK IMPLEMENTATION

## 3.1 Structure des fichiers

```
web-sdk/apps/wc86/
├── .storybook/
│   ├── main.ts                    # Config Storybook
│   └── preview.ts
├── package.json
├── svelte.config.js
├── tsconfig.json
├── vite.config.ts
├── lingui.config.ts
├── .eslintrc.cjs
│
├── src/
│   ├── app.html                   # Template HTML
│   │
│   ├── game/                      # 17 fichiers TypeScript
│   │   ├── actor.ts               # XState game actor
│   │   ├── assets.ts              # Déclaration assets
│   │   ├── bookEventHandlerMap.ts # Handlers événements RGS
│   │   ├── config.ts              # Config jeu (miroir math-sdk)
│   │   ├── constants.ts           # Constantes + SYMBOL_INFO_MAP
│   │   ├── context.ts             # Contexte Svelte
│   │   ├── eventEmitter.ts        # Event emitter typé
│   │   ├── sound.ts               # Config sons
│   │   ├── stateApp.ts            # État application
│   │   ├── stateGame.svelte.ts    # État jeu réactif
│   │   ├── stateLayout.ts         # Layout responsif
│   │   ├── stateXstate.ts         # Machine XState
│   │   ├── types.ts               # Types de base
│   │   ├── typesBookEvent.ts      # Types événements RGS
│   │   ├── typesEmitterEvent.ts   # Types événements UI
│   │   ├── utils.ts               # Utilitaires
│   │   └── winLevelMap.ts         # Niveaux de gain
│   │
│   ├── components/                # 38 composants Svelte
│   │   ├── Game.svelte            # Composant racine
│   │   ├── Background.svelte
│   │   ├── Board.svelte
│   │   ├── BoardBase.svelte
│   │   ├── BoardContainer.svelte
│   │   ├── BoardFrame.svelte
│   │   ├── BoardMask.svelte
│   │   ├── Symbol.svelte
│   │   ├── SymbolSpine.svelte
│   │   ├── SymbolSprite.svelte
│   │   ├── SymbolWrap.svelte
│   │   ├── ReelSymbol.svelte
│   │   ├── TumbleBoard.svelte
│   │   ├── TumbleBoardBase.svelte
│   │   ├── TumbleSymbol.svelte
│   │   ├── Anticipation.svelte
│   │   ├── Anticipations.svelte
│   │   ├── Win.svelte
│   │   ├── WinAnimation.svelte
│   │   ├── WinCoins.svelte
│   │   ├── FreeSpinIntro.svelte
│   │   ├── FreeSpinOutro.svelte
│   │   ├── FreeSpinCounter.svelte
│   │   ├── FreeSpinAnimation.svelte
│   │   ├── Transition.svelte
│   │   ├── TransitionAnimation.svelte
│   │   ├── LoadingScreen.svelte
│   │   ├── PressToContinue.svelte
│   │   ├── Sound.svelte
│   │   ├── EnableSound.svelte
│   │   ├── EnableGameActor.svelte
│   │   ├── ResumeBet.svelte
│   │   ├── I18nTest.svelte
│   │   │
│   │   │ # === NOUVEAUX COMPOSANTS WC86 ===
│   │   ├── HuntMultiplier.svelte        # Affichage x1→x500
│   │   ├── HowlChainEffect.svelte       # Animation chaîne wilds
│   │   ├── PackSplitAnimation.svelte    # Animation split Alpha Wolf
│   │   ├── TerritoryExpand.svelte       # Animation expansion grille
│   │   ├── GridExpansion.svelte         # Transition grilles
│   │   ├── AlphaDominationIntro.svelte  # Intro super bonus
│   │   └── VolatilitySelector.svelte    # Sélection mode
│   │
│   ├── routes/
│   │   ├── +layout.svelte
│   │   ├── +layout.ts
│   │   └── +page.svelte
│   │
│   ├── stories/
│   │   ├── ComponentsGame.stories.svelte
│   │   ├── ComponentsSymbol.stories.svelte
│   │   ├── ModeBaseBook.stories.svelte
│   │   ├── ModeBaseBookEvent.stories.svelte
│   │   ├── ModeBonusBook.stories.svelte
│   │   ├── ModeBonusBookEvent.stories.svelte
│   │   └── data/
│   │       ├── base_books.ts
│   │       ├── base_events.ts
│   │       ├── bonus_books.ts
│   │       └── bonus_events.ts
│   │
│   └── i18n/
│       ├── i18nDerived.ts
│       └── messagesMap/
│           ├── en.ts
│           ├── zh.ts
│           └── index.ts
│
└── static/assets/
    ├── audio/                     # Sons
    ├── fonts/                     # Polices bitmap
    ├── spines/                    # Animations Spine
    └── sprites/                   # Sprites
```

## 3.2 package.json

```json
{
  "name": "wc86",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "vite dev --host --port 3002",
    "build": "vite build",
    "preview": "vite preview",
    "storybook": "PUBLIC_CHROMATIC=true storybook dev -p 6002 public",
    "build-storybook": "storybook build",
    "check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
    "lint": "eslint \"src\"",
    "format": "prettier --write --ignore-path=../../.prettierignore ."
  },
  "dependencies": {
    "svelte": "^5.20.5",
    "@sveltejs/kit": "^2.17.3",
    "@lingui/core": "^5.2.0",
    "lodash": "^4.17.21",

    "pixi-svelte": "workspace:*",
    "state-shared": "workspace:*",
    "constants-shared": "workspace:*",
    "envs": "workspace:*",
    "rgs-requests": "workspace:*",

    "utils-xstate": "workspace:*",
    "utils-slots": "workspace:*",
    "utils-book": "workspace:*",
    "utils-bet": "workspace:*",
    "utils-sound": "workspace:*",
    "utils-shared": "workspace:*",
    "utils-event-emitter": "workspace:*",
    "utils-layout": "workspace:*",

    "components-pixi": "workspace:*",
    "components-ui-pixi": "workspace:*",
    "components-ui-html": "workspace:*",
    "components-layout": "workspace:*",
    "components-shared": "workspace:*"
  },
  "devDependencies": {
    "@sveltejs/adapter-static": "^3.0.0",
    "@sveltejs/vite-plugin-svelte": "^4.0.0",
    "vite": "^6.2.0",
    "typescript": "^5.6.0",
    "@storybook/svelte": "^8.0.0",
    "config-ts": "workspace:*",
    "config-vite": "workspace:*",
    "config-svelte": "workspace:*",
    "config-storybook": "workspace:*",
    "config-lingui": "workspace:*",
    "eslint-config-custom": "workspace:*"
  }
}
```

## 3.3 Fichiers game/ détaillés

### types.ts
```typescript
import type config from './config';

export type SymbolName = keyof typeof config.symbols;
export type RawSymbol = {
  name: SymbolName;
  multiplier?: number;
  scatter?: boolean;
  wild?: boolean;
  splitWild?: boolean;
  howlingWild?: boolean;
  territory?: boolean;
};

export type BetMode = 'base' | 'pack_hunt' | 'pack_hunt_plus' | 'alpha_domination';
export type GameType = 'basegame' | 'freegame' | 'alphaDomination';
export type GridConfig = '6x5' | '7x6' | '8x7' | '8x8';
export type VolatilityMode = 'LONE_WOLF' | 'PACK' | 'ALPHA';

export const SYMBOL_STATES = [
  'static', 'spin', 'land', 'win', 'postWinStatic',
  'explosion', 'split', 'howl', 'territory'
] as const;

export type SymbolState = (typeof SYMBOL_STATES)[number];
export type Position = { reel: number; row: number };
```

### typesBookEvent.ts
```typescript
import type { BetType } from 'rgs-requests';
import type { SymbolName, RawSymbol, GameType, Position, GridConfig } from './types';

// === STANDARD EVENTS ===
type BookEventReveal = {
  index: number;
  type: 'reveal';
  board: RawSymbol[][];
  paddingPositions: number[];
  anticipation: number[];
  gameType: GameType;
  currentGrid?: GridConfig;
};

type BookEventWinInfo = {
  index: number;
  type: 'winInfo';
  totalWin: number;
  wins: {
    symbol: SymbolName;
    kind: number;
    win: number;
    positions: Position[];
    meta: { ways: number; globalMult: number; huntMultiplier: number };
  }[];
};

type BookEventTumbleBoard = {
  index: number;
  type: 'tumbleBoard';
  explodingSymbols: Position[];
  newSymbols: RawSymbol[][];
};

type BookEventUpdateHuntMultiplier = {
  index: number;
  type: 'updateHuntMultiplier';
  huntMultiplier: number;
  cascadeCount: number;
  multCap: number;
};

type BookEventPackSplit = {
  index: number;
  type: 'packSplit';
  alphaPosition: Position;
  targetSymbol: SymbolName;
  splitMultiplier: number;
};

type BookEventHowlChain = {
  index: number;
  type: 'howlChain';
  wildPositions: Position[];
  wildCount: number;
  chainType: 'additive' | 'multiplicative';
  chainMultiplier: number;
};

type BookEventTerritoryExpand = {
  index: number;
  type: 'territoryExpand';
  newGrid: GridConfig;
  newReels: number;
  newRows: number[];
  waysCount: number;
};

type BookEventAlphaDominationStart = {
  index: number;
  type: 'alphaDominationStart';
  fixedGrid: '8x8';
  startingMultiplier: number;
  multCap: number;
};

// ... autres événements standard (freeSpinTrigger, setWin, etc.)

export type BookEvent =
  | BookEventReveal
  | BookEventWinInfo
  | BookEventTumbleBoard
  | BookEventUpdateHuntMultiplier
  | BookEventPackSplit
  | BookEventHowlChain
  | BookEventTerritoryExpand
  | BookEventAlphaDominationStart
  // ... autres
  ;

export type Bet = BetType<BookEvent>;
```

### bookEventHandlerMap.ts (extrait)
```typescript
import { stateBet } from 'state-shared';
import { eventEmitter } from './eventEmitter';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import type { BookEvent, BookEventContext } from './typesBookEvent';

export const bookEventHandlerMap = {
  reveal: async (event, { bookEvents }) => {
    stateGame.gameType = event.gameType;
    if (event.currentGrid) stateGame.currentGrid = event.currentGrid;
    await stateGameDerived.enhancedBoard.spin({ revealEvent: event });
  },

  updateHuntMultiplier: async (event) => {
    eventEmitter.broadcast({ type: 'huntMultiplierShow' });
    eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up' });
    await eventEmitter.broadcastAsync({
      type: 'huntMultiplierUpdate',
      multiplier: event.huntMultiplier,
      cascadeCount: event.cascadeCount,
      isMaxed: event.huntMultiplier >= event.multCap
    });
  },

  packSplit: async (event) => {
    eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_pack_split' });
    await eventEmitter.broadcastAsync({
      type: 'packSplitAnimate',
      alphaPosition: event.alphaPosition,
      targetSymbol: event.targetSymbol,
      splitMultiplier: event.splitMultiplier
    });
  },

  howlChain: async (event) => {
    const sound = event.chainType === 'multiplicative'
      ? 'sfx_howl_chain_multi'
      : 'sfx_howl_chain_add';
    eventEmitter.broadcast({ type: 'soundOnce', name: sound });
    await eventEmitter.broadcastAsync({
      type: 'howlChainAnimate',
      positions: event.wildPositions,
      chainType: event.chainType,
      chainMultiplier: event.chainMultiplier
    });
  },

  territoryExpand: async (event) => {
    eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_territory_expand' });
    await eventEmitter.broadcastAsync({ type: 'uiHide' });
    await eventEmitter.broadcastAsync({
      type: 'gridExpand',
      newGrid: event.newGrid,
      waysCount: event.waysCount
    });
    stateGame.currentGrid = event.newGrid;
    await eventEmitter.broadcastAsync({ type: 'uiShow' });
  },

  alphaDominationStart: async (event) => {
    await eventEmitter.broadcastAsync({ type: 'transition' });
    eventEmitter.broadcast({ type: 'alphaDominationIntroShow' });
    eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_alpha_domination' });
    await eventEmitter.broadcastAsync({
      type: 'alphaDominationIntroUpdate',
      startingMult: event.startingMultiplier
    });
    stateGame.gameType = 'alphaDomination';
    stateGame.currentGrid = '8x8';
  },

  // ... autres handlers
};
```

---

# PARTIE 4: ASSETS À CRÉER (100%)

## 4.1 AUDIO - 60 fichiers

### Fichiers audio
```
static/assets/audio/
├── sounds.mp3          # ~5 MB - Audio principal
├── sounds.ogg          # ~4 MB - Fallback OGG
├── sounds.m4a          # ~4 MB - Fallback M4A
├── sounds.ac3          # ~5 MB - Fallback AC3
└── sounds.json         # ~6 KB - Définition sprites
```

### sounds.json - 60 sprites audio

**Musiques de fond (8):**
| Nom | Durée | Loop | Description |
|-----|-------|------|-------------|
| `bgm_main` | 132s | ✓ | Lo-fi hip-hop chill |
| `bgm_freespin` | 69s | ✓ | Synthwave agressif |
| `bgm_alpha_domination` | 90s | ✓ | Epic orchestral |
| `bgm_winlevel_big` | 8s | ✓ | Big win theme |
| `bgm_winlevel_superwin` | 8s | ✓ | Super win theme |
| `bgm_winlevel_mega` | 8s | ✓ | Mega win theme |
| `bgm_winlevel_epic` | 8s | ✓ | Epic win theme |
| `bgm_winlevel_max` | 8s | ✓ | Max win theme |

**Jingles (3):**
| Nom | Durée | Description |
|-----|-------|-------------|
| `jng_intro_fs` | 2s | Intro free spins |
| `jng_alpha_domination` | 3s | Intro Alpha Domination |
| `jng_territory_expand` | 2s | Expansion grille |

**Effets - Reel stops (6):**
| Nom | Durée |
|-----|-------|
| `sfx_reel_stop_1` → `sfx_reel_stop_6` | 0.25s chacun |

**Effets - Scatter (7):**
| Nom | Durée |
|-----|-------|
| `sfx_scatter_stop_1` → `sfx_scatter_stop_6` | 1s chacun |
| `sfx_scatter_win` | 4s |

**Effets - Multiplicateurs (10):**
| Nom | Durée | Description |
|-----|-------|-------------|
| `sfx_multiplier_up` | 1.5s | Multiplicateur augmente |
| `sfx_multiplier_landing` | 1s | Atterrissage mult |
| `sfx_multiplier_reset` | 0.5s | Reset mult |
| `sfx_multiplier_win` | 4s | Win avec mult |
| `sfx_multiplier_combine_a` | 1s | Howl Chain combine |
| `sfx_multiplier_combine_b` | 1s | Howl Chain combine |
| `sfx_multiplier_explosion_a` | 1s | Explosion |
| `sfx_multiplier_explosion_b` | 2s | Explosion |
| `sfx_multiplier_explosion_c` | 1s | Explosion |
| `sfx_multiplier_update` | 1.5s | Update |

**Effets - Features WC86 (10):**
| Nom | Durée | Description |
|-----|-------|-------------|
| `sfx_pack_split` | 2s | Alpha Wolf split |
| `sfx_howl_chain_add` | 1.5s | Howl Chain additif |
| `sfx_howl_chain_multi` | 2.5s | Howl Chain multiplicatif |
| `sfx_territory_expand` | 3s | Expansion grille |
| `sfx_alpha_domination_intro` | 4s | Intro super bonus |
| `sfx_wolf_howl_1` | 2s | Hurlement loup |
| `sfx_wolf_howl_2` | 2.5s | Hurlement loup |
| `sfx_cascade_explosion` | 1s | Explosion cascade |
| `sfx_symbols_landing` | 1.2s | Atterrissage symboles |
| `sfx_wild_explode` | 1.4s | Explosion wild |

**Effets - Wins (10):**
| Nom | Durée |
|-----|-------|
| `sfx_winlevel_small` | 1s |
| `sfx_winlevel_standard` | 1.2s |
| `sfx_winlevel_substantial` | 2.5s |
| `sfx_winlevel_nice` | 1.5s |
| `sfx_winlevel_end` | 2s |
| `sfx_bigwin_coinloop` | 17s (loop) |
| `sfx_youwon_panel` | 3s |
| `tumble_win_1` → `tumble_win_5` | 1s chacun |

**Effets - UI (6):**
| Nom | Durée |
|-----|-------|
| `sfx_btn_general` | 0.06s |
| `sfx_btn_spin` | 1s |
| `sfx_anticipation` | 8s |
| `sfx_anticipation_start` | 1s |
| `sfx_fs_respins` | 4s |
| `sfx_superfreespin` | 6s |

---

## 4.2 FONTS - 4 dossiers

```
static/assets/fonts/
├── alphaFont/                 # NOUVEAU - Style crypto/wolf
│   ├── alpha_font.png
│   ├── alpha_font.webp
│   ├── alpha_font.json
│   ├── alpha_font.xml
│   └── index.ts
├── goldFont/                  # Wins dorés
│   ├── mm_gold.png
│   ├── mm_gold.webp
│   ├── mm_gold.json
│   ├── mm_gold.xml
│   └── index.ts
├── silverFont/                # Texte argenté
│   ├── mm_silver.png
│   ├── mm_silver.json
│   ├── mm_silver.xml
│   └── index.ts
└── cryptoFont/                # NOUVEAU - Crypto symbols
    ├── crypto_font.png
    ├── crypto_font.webp
    ├── crypto_font.json
    ├── crypto_font.xml
    └── index.ts
```

**Caractères requis par font:**
- Chiffres: 0-9
- Lettres: A-Z
- Symboles: + - . , : ! ? x X $ € ₿

---

## 4.3 SPINES - 20 dossiers

### Symboles - 12 dossiers

```
static/assets/spines/symbols/
├── boss_wolf/
│   ├── boss_wolf.png (~500 KB)
│   ├── boss_wolf.webp (~200 KB)
│   ├── boss_wolf.atlas
│   ├── boss_wolf.json
│   └── index.ts
│   Animations: static, land, win, idle
│
├── hustler/
│   Animations: static, land, win, idle
│
├── tech_bro/
│   Animations: static, land, win, idle
│
├── diamond_hands/
│   Animations: static, land, win, idle
│
├── cocktail/                  # Martini neon style 80s
│   Animations: static, land, win, glow
│
├── vip_card/                  # Carte membre doree
│   Animations: static, land, win, glow
│
├── disco_ball/                # Boule disco brillante
│   Animations: static, land, win, glow
│
├── dice/                      # Des lumineux neon
│   Animations: static, land, win, glow
│
├── alpha_wolf/                # SPECIAL - Split Wild
│   Animations: static, land, win, spin, split_charge, split_release
│
├── howling_wild/              # SPECIAL - Multiplicateur
│   Animations: static, land, win, howl_idle, howl_chain
│   + Slots pour affichage multiplicateur (x2, x3, x5, x10, x15)
│
├── moon_scatter/              # SPECIAL - Scatter
│   Animations: static, land, spin, win, glow
│
└── territory/                 # SPECIAL - Territory
    Animations: static, land, win, collect, glow
```

### Effets - 8 dossiers

```
static/assets/spines/

├── huntMultiplier/            # Multiplicateur Hunt Cascade
│   ├── hunt_mult.png
│   ├── hunt_mult.webp
│   ├── hunt_mult.atlas
│   ├── hunt_mult.json
│   └── index.ts
│   Animations: static, increment, maxed, reset, win
│
├── howlChain/                 # Effet chaîne Howling Wild
│   Animations: chain_add, chain_multiply, connection_line, multiplier_reveal
│
├── packSplit/                 # Effet Pack Split
│   Animations: alpha_charge, split_wave, symbol_duplicate
│
├── territoryExpand/           # Expansion grille
│   Animations: expand_6x5_to_7x6, expand_7x6_to_8x7, expand_8x7_to_8x8
│
├── alphaDomination/           # Super bonus intro
│   Animations: intro, idle, transition_in, transition_out
│
├── bigwin/                    # Big wins
│   Animations: big_win_intro/idle/exit, super_win_*, mega_win_*, epic_win_*, max_win_*
│
├── transition/                # Transitions
│   Animations: transition_in, transition_out
│
├── anticipation/              # Anticipation scatter
│   Animations: anticipation_intro, anticipation_loop, anticipation_out
│
├── fsIntro/                   # Intro free spins
│   Animations: fs_screen_intro, fs_screen_idle, fs_number
│
├── loader/                    # Écran de chargement
│   Animations: title_screen
│
├── tumbleWin/                 # Effet tumble win
│   Animations: explosion, idle
│
├── globalMultiplier/          # Frame multiplicateur
│   Animations: static, increment, reset, win
│
├── reelhouse/                 # Glow cadre reels
│   Animations: glow_start, glow_idle, glow_exit
│
├── foregroundAnimation/       # Animation fond base
│   Animations: dust, idle
│
└── foregroundFeatureAnimation/ # Animation fond feature
    Animations: dust, idle
```

---

## 4.4 SPRITES - 10 dossiers

```
static/assets/sprites/

├── symbolsStatic/             # Symboles statiques (12 symboles)
│   ├── symbolsStatic.png (~1 MB)
│   ├── symbolsStatic.webp (~600 KB)
│   ├── symbolsStatic.json
│   └── index.ts
│   Frames: boss_wolf, hustler, tech_bro, diamond_hands,
│           cocktail, vip_card, disco_ball, dice,
│           alpha_wolf, howling_wild, moon_scatter, territory
│
├── reelsFrame/                # Cadres reels (4 tailles)
│   Frames: frame_6x5, frame_7x6, frame_8x7, frame_8x8, frame_glow
│
├── freeSpins/                 # Affichage FS
│   Frames: fs_panel, fs_numbers (0-9), fs_text
│
├── coin/                      # Animation pièces (12 frames)
│
├── progressBar/               # Barre chargement (3 frames)
│
├── pressToContinueText/       # Texte "appuyer" (16 frames multilingue)
│
├── winSmall/                  # Labels win small (17 frames)
│
├── payFrame/                  # Cadre paytable
│
├── uiAssets/                  # Boutons UI custom
│   Frames: autospin_active, autospin_active_hover,
│           turbo_active, turbo_active_hover,
│           volatility_lone, volatility_pack, volatility_alpha
│
└── backgrounds/               # NOUVEAU - Fonds
    Frames: bg_base, bg_freespin, bg_alpha_domination
```

---

## 4.5 RÉSUMÉ ASSETS

| Catégorie | Dossiers | Fichiers | Taille estimée |
|-----------|----------|----------|----------------|
| Audio | 1 | 5 | ~20 MB |
| Fonts | 4 | 20 | ~5 MB |
| Spines | 20 | 80 | ~30 MB |
| Sprites | 10 | 40 | ~15 MB |
| **TOTAL** | **35** | **145** | **~70 MB** |

---

# PARTIE 5: INTÉGRATION & TESTS

## 5.1 Mapping événements Math-SDK → Web-SDK

| Math Event (Python) | Book Event (TS) | Handler Action |
|---------------------|-----------------|----------------|
| `reveal_event()` | `reveal` | Spin board, set gameType/grid |
| `win_info_event()` | `winInfo` | Animate winning symbols |
| `tumble_board_event()` | `tumbleBoard` | Explode → slide → settle |
| `update_global_mult_event()` | `updateHuntMultiplier` | Update hunt multiplier UI |
| `pack_split_event()` | `packSplit` | Alpha Wolf split animation |
| `howl_chain_event()` | `howlChain` | Howl Chain effect |
| `territory_expand_event()` | `territoryExpand` | Grid expansion |
| `alpha_domination_start_event()` | `alphaDominationStart` | Super bonus intro |
| `fs_trigger_event()` | `freeSpinTrigger` | Free spins intro |
| `update_freespin_event()` | `updateFreeSpin` | Update FS counter |
| `freespin_end_event()` | `freeSpinEnd` | Free spins outro |
| `set_win_event()` | `setWin` | Big win celebration |
| `set_total_event()` | `setTotalWin` | Update total win |
| `volatility_mode_event()` | `volatilityModeChange` | Mode change UI |

## 5.2 Tests Math-SDK

```bash
# 1. Simulations
cd math-sdk/games/wc86
python run.py

# Vérifier:
# - 500k+ simulations base mode
# - RTP dans 96.2%-96.8% selon volatilité
# - Hit rates cohérents
# - Distribution gains correcte

# 2. Optimisation Rust
# Vérifier optimization_files/ générés
# - trial_results/
# - lookup_base_optimized.csv
# - lookup_pack_hunt_optimized.csv
# etc.

# 3. Analyse
# Vérifier library/
# - books_*.json
# - lookUpTable_*.csv
# - configs/*.json
```

## 5.3 Tests Web-SDK

```bash
# 1. Dev server
cd web-sdk/apps/wc86
pnpm dev

# 2. Storybook
pnpm storybook

# 3. Build
pnpm build

# 4. Type check
pnpm check
```

## 5.4 Tests fonctionnels

- [ ] Spin base game
- [ ] Hunt Cascade (tumble + mult increment)
- [ ] Pack Split (Alpha Wolf)
- [ ] Howl Chain (2 wilds = add, 3+ = mult)
- [ ] Territory Expand (3/6/10 → grid change)
- [ ] Free Spins trigger (3+ scatters)
- [ ] Free Spins persistent multiplier
- [ ] Alpha Domination (8x8, x5 min)
- [ ] Feature Buy (75x, 150x, 500x)
- [ ] 3 volatility modes
- [ ] Big wins (all levels)
- [ ] Resume bet
- [ ] Responsive (desktop, tablet, portrait)
- [ ] Audio on/off
- [ ] Turbo mode
- [ ] Auto spin

---

# ANNEXE: CHECKLIST IMPLÉMENTATION

## Math-SDK (20 fichiers)
- [ ] `__init__.py`
- [ ] `game_config.py`
- [ ] `gamestate.py`
- [ ] `game_override.py`
- [ ] `game_executables.py`
- [ ] `game_calculations.py`
- [ ] `game_events.py`
- [ ] `game_optimization.py`
- [ ] `run.py`
- [ ] `README.md`
- [ ] `reels/BR_LONE_WOLF.csv`
- [ ] `reels/BR_PACK.csv`
- [ ] `reels/BR_ALPHA.csv`
- [ ] `reels/FR_LONE_WOLF.csv`
- [ ] `reels/FR_PACK.csv`
- [ ] `reels/FR_ALPHA.csv`
- [ ] `reels/FR_WINCAP_LONE.csv`
- [ ] `reels/FR_WINCAP_PACK.csv`
- [ ] `reels/FR_WINCAP_ALPHA.csv`
- [ ] `reels/AD_BASE.csv`
- [ ] `reels/AD_WINCAP.csv`

## Web-SDK game/ (17 fichiers)
- [ ] `actor.ts`
- [ ] `assets.ts`
- [ ] `bookEventHandlerMap.ts`
- [ ] `config.ts`
- [ ] `constants.ts`
- [ ] `context.ts`
- [ ] `eventEmitter.ts`
- [ ] `sound.ts`
- [ ] `stateApp.ts`
- [ ] `stateGame.svelte.ts`
- [ ] `stateLayout.ts`
- [ ] `stateXstate.ts`
- [ ] `types.ts`
- [ ] `typesBookEvent.ts`
- [ ] `typesEmitterEvent.ts`
- [ ] `utils.ts`
- [ ] `winLevelMap.ts`

## Web-SDK components/ (38 fichiers)
- [ ] Core: Game, Background, Board, Symbol, Win, Transition...
- [ ] NOUVEAUX: HuntMultiplier, HowlChainEffect, PackSplitAnimation, TerritoryExpand, GridExpansion, AlphaDominationIntro, VolatilitySelector

## Assets (145 fichiers)
- [ ] Audio: 5 fichiers + sounds.json (60 sprites)
- [ ] Fonts: 4 dossiers
- [ ] Spines: 20 dossiers
- [ ] Sprites: 10 dossiers

---

**FIN DU PLAN D'IMPLÉMENTATION**

Ce document est la référence complète pour l'implémentation d'WC86.
Tous les SDK Stake sont utilisés. Tous les fichiers sont listés.