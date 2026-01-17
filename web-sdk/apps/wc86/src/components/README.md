# WC86 - Wolf Club 86 - Components

## Context pour Claude (STEPH)
Tu travailles sur les **Composants Svelte** du jeu WC86 - Wolf Club 86. Theme: Nightclub retro 80s avec des loups. Ce README te donne tout le contexte necessaire.

## Architecture

### Stack
- Svelte 5 avec runes ($state, $derived, $effect)
- PixiJS 8 via pixi-svelte
- Spine animations (pixi-spine)
- GSAP pour animations complexes (optionnel)

### Packages Stake a utiliser
```typescript
// PixiJS components
import { Sprite, AnimatedSprite, Container, Text } from 'pixi-svelte';
import { Spine, SpineProvider } from 'components-pixi';

// Layout
import { MainContainer } from 'components-layout';

// UI
import { UI, UiGameName, ButtonBuyBonus } from 'components-ui-pixi';
import { Modals, GlobalStyle } from 'components-ui-html';

// Shared
import { Authenticate, LoaderStakeEngine, EnableHotkey } from 'components-shared';
```

## Composants core/ (adapte de ways)

### Board Components
| Component | Role |
|-----------|------|
| `Board.svelte` | Container principal du board |
| `BoardBase.svelte` | Gestion du background |
| `BoardContainer.svelte` | Positionnement responsive |
| `BoardFrame.svelte` | Cadre de la grille |
| `BoardMask.svelte` | Masque pour overflow |

### Symbol Components
| Component | Role |
|-----------|------|
| `Symbol.svelte` | Wrapper symbol (switch sprite/spine) |
| `SymbolSpine.svelte` | Animation spine d'un symbole |
| `SymbolSprite.svelte` | Sprite statique d'un symbole |

### Tumble Components
| Component | Role |
|-----------|------|
| `TumbleBoard.svelte` | Board avec cascade |
| `TumbleBoardBase.svelte` | Base pour tumble |
| `TumbleSymbol.svelte` | Symbole qui cascade |

### Win Components
| Component | Role |
|-----------|------|
| `Win.svelte` | Container wins |
| `WinAnimation.svelte` | Big win animation |
| `WinCoins.svelte` | Particules coins |

### Free Spin Components
| Component | Role |
|-----------|------|
| `FreeSpinIntro.svelte` | Intro animation FS |
| `FreeSpinOutro.svelte` | Outro avec total win |
| `FreeSpinCounter.svelte` | Compteur spins restants |

### Transition Components
| Component | Role |
|-----------|------|
| `Transition.svelte` | Transition base↔FS |
| `TransitionAnimation.svelte` | Animation de transition |

### Autres
| Component | Role |
|-----------|------|
| `Game.svelte` | Root component |
| `Background.svelte` | Background anime |
| `LoadingScreen.svelte` | Ecran de chargement |

## Composants custom/ (nouveaux)

### HuntMultiplier.svelte
```svelte
<script lang="ts">
  import { Spine } from 'components-pixi';
  import { eventEmitter } from '$game/eventEmitter';

  let { visible = false } = $props();
  let multiplier = $state(1);
  let animation = $state('idle');

  $effect(() => {
    eventEmitter.on('huntMultiplierShow', () => { visible = true; });
    eventEmitter.on('huntMultiplierUpdate', (data) => {
      multiplier = data.value;
      animation = 'increase';
    });
    eventEmitter.on('huntMultiplierHide', () => { visible = false; });
  });
</script>

{#if visible}
  <Spine
    src="effects/huntMultiplier/huntMultiplier"
    animation={animation}
    onComplete={() => animation = 'idle'}
  />
  <Text text={`x${multiplier}`} style={multiplierTextStyle} />
{/if}
```

### HowlChainEffect.svelte
- Affiche connections entre wilds adjacents
- Animation differente pour additive vs multiplicative
- Affiche le multiplier chain total

### PackSplitAnimation.svelte
- Animation de l'Alpha Wolf qui se split
- Duplications vers la gauche
- Effet visuel x2, x3, x4

### TerritoryExpand.svelte
- Animation de collect du territory
- Progress bar vers prochaine expansion

### GridExpansion.svelte
- Animation de transition de grille
- 6x5 → 7x6 → 8x7 → 8x8
- Resize smooth des symboles

### AlphaDominationIntro.svelte
- Intro cinematique pour super bonus
- Affiche starting multiplier et cap
- Transition vers 8x8 grid

### VolatilitySelector.svelte
- Selection LONE_WOLF / PACK / ALPHA
- Affiche RTP et max win de chaque mode

## Emitter Events a ecouter

```typescript
// Recus de ELI
eventEmitter.on('boardSpin', () => { /* start spin animation */ });
eventEmitter.on('boardReveal', () => { /* reveal symbols */ });
eventEmitter.on('symbolWin', (positions) => { /* animate winning symbols */ });
eventEmitter.on('symbolExplode', (positions) => { /* explode symbols */ });
eventEmitter.on('huntMultiplierShow', () => { /* show multiplier */ });
eventEmitter.on('huntMultiplierUpdate', (data) => { /* update value */ });
eventEmitter.on('packSplitAnimate', (data) => { /* play split animation */ });
eventEmitter.on('howlChainAnimate', (data) => { /* draw chain connections */ });
eventEmitter.on('gridExpand', (data) => { /* expand grid animation */ });
// ... etc
```

## Assets requis (de ARIE)

### Spine paths
```typescript
// Symboles
'spines/symbols/boss_wolf/boss_wolf'
'spines/symbols/alpha_wolf/alpha_wolf'
// ... etc

// Effets
'spines/effects/huntMultiplier/huntMultiplier'
'spines/effects/howlChain/howlChain'
'spines/effects/packSplit/packSplit'
'spines/effects/bigwin/bigwin'
// ... etc
```

### Animations requises
Voir `docs/INTEGRATION_CONTRACT.md` section "REQUIRED_ANIMATIONS"

## Storybook

### Stories a creer
1. `base_books.stories.ts` - Livre de jeu base
2. `bonus_books.stories.ts` - Livre avec FS et features
3. `components.stories.ts` - Composants individuels

### Data
Creer des mock books dans `stories/data/`:
- `baseWin.json` - Simple win
- `cascadeWin.json` - Multiple cascades
- `packSplit.json` - Pack split feature
- `howlChain.json` - Howl chain feature
- `freeSpins.json` - Full FS session
- `alphaDomination.json` - Super bonus

## Fichiers a creer

```
components/
├── core/
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
├── custom/
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
└── stories/
    ├── base_books.stories.ts
    ├── bonus_books.stories.ts
    └── components.stories.ts
```