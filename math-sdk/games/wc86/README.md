# WC86 - Wolf Club 86 - Math SDK

## Context pour Claude (DAN)
Tu travailles sur le **Math Engine** du jeu WC86 - Wolf Club 86. Theme: Nightclub retro 80s avec des loups. Ce README te donne tout le contexte necessaire.

## Game Mechanics

### Grille Dynamique
- Base: 6 reels x 5 rows = 7,776 ways
- Expand: 7x6 (46,656) → 8x7 (117,649) → 8x8 (262,144 ways)
- Trigger: Collecte de symboles TERRITORY (3→7x6, 6→8x7, 10→8x8)

### Volatility Modes
| Mode | RTP | Max Win | FS Mult Cap |
|------|-----|---------|-------------|
| LONE_WOLF | 96.8% | 10,000x | 50 |
| PACK | 96.5% | 25,000x | 200 |
| ALPHA | 96.2% | 50,000x | 500 |

### Symboles (12)
**Premium - Wolves (pays L→R):**
- BOSS_WOLF: 50/25/10/5 (6/5/4/3 of a kind) - Le patron du club
- HUSTLER: 30/15/6/3 - Loup streetwear, chaines, confiant
- TECH_BRO: 20/10/4/2 - Loup geek avec lunettes
- DIAMOND_HANDS: 15/7.5/3/1.5 - High roller

**Low - Club items:**
- COCKTAIL: 5/2.5/1/0.5 - Martini neon style 80s
- VIP_CARD: 4/2/0.8/0.4 - Carte membre doree
- DISCO_BALL: 3/1.5/0.6/0.3 - Boule disco brillante
- DICE: 2/1/0.4/0.2 - Des lumineux neon

**Special:**
- ALPHA_WOLF: Wild, triggers Pack Split
- HOWLING_WILD: Wild avec multiplier (x2-x15), Howl Chain
- MOON_SCATTER: Trigger Free Spins
- TERRITORY: Collectible pour grid expand

### Features

#### Hunt Cascade (Tumble)
- Symboles gagnants explosent
- Nouveaux symboles tombent
- Multiplicateur +1 par cascade
- Cap: 50 (base), 200-500 (FS selon mode)

#### Pack Split
- Quand ALPHA_WOLF land
- Duplique sur positions a gauche
- 2-4 duplications possibles
- Multiplicateur cumulatif: x2, x3, x4

#### Howl Chain
- 2+ HOWLING_WILD adjacents (4-directions)
- 2 wilds: ADDITIF (sum des multipliers)
- 3+ wilds: MULTIPLICATIF (product)

#### Territory Expand
- Collecte TERRITORY symbols
- 3 → 7x6 grid
- 6 → 8x7 grid
- 10 → 8x8 grid
- Persiste pendant session FS

#### Pack Hunt (Free Spins)
- 3/4/5/6 MOON_SCATTER = 10/12/15/20 spins
- Multiplicateur persiste entre spins
- Retrigger: 2/3/4/5/6 scatter = +3/5/8/10/15

#### Alpha Domination (500x bet)
- Grille fixe 8x8
- Start mult: x5 minimum
- Mult cap: 500
- Guaranteed Alpha Wolves par spin

### Bet Modes
| Mode | Cost | Description |
|------|------|-------------|
| base | 1.0x | Normal play |
| pack_hunt | 75x | Buy Free Spins |
| pack_hunt_plus | 150x | Buy FS, start x3 |
| alpha_domination | 500x | Buy super bonus |

## SDK Stake a utiliser

### Imports requis
```python
# Config
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode

# Calculations
from src.calculations.symbol import Symbol
from src.calculations.board import Board
from src.calculations.ways import Ways
from src.calculations.tumble import Tumble

# State
from src.state.general_game_state import GeneralGameState
from src.state.conditions import Conditions
from src.state.book import Book

# Events
from src.events.events import (
    reveal_event, win_info_event, tumble_board_event,
    fs_trigger_event, freespin_end_event, set_win_event
)

# Wins
from src.wins.win_manager import WinManager
```

### Rust Optimization
```python
from optimization_program.optimization_execution import OptimizationExecution
from optimization_program.construct_scaling import ConstructScaling
from optimization_program.construct_parameters import ConstructParameters
```

## Fichiers a creer

1. **game_config.py** (~300 lignes)
   - Class GameConfig(Config)
   - Paytable, symbols, bet modes, volatility modes

2. **gamestate.py** (~150 lignes)
   - Class GameState(GameStateOverride)
   - run_spin(), run_freespin(), run_alpha_domination()

3. **game_override.py** (~120 lignes)
   - Class GameStateOverride(GameExecutables)
   - assign_special_sym_function(), reset_book()

4. **game_executables.py** (~80 lignes)
   - Class GameExecutables(GameCalculations)
   - evaluate_ways_board_with_wilds(), find_adjacent_howling_wilds()

5. **game_calculations.py** (~30 lignes)
   - Class GameCalculations(Executables)
   - calculate_ways_count()

6. **game_events.py** (~100 lignes)
   - territory_expand_event(), pack_split_event()
   - howl_chain_event(), alpha_domination_start_event()
   - update_hunt_multiplier_event()

7. **game_optimization.py** (~180 lignes)
   - Class OptimizationSetup
   - Setup pour 4 bet modes

8. **run.py** (~80 lignes)
   - Main entry, orchestration

9. **reels/*.csv** (11 fichiers)
   - BR_LONE_WOLF, BR_PACK, BR_ALPHA
   - FR_LONE_WOLF, FR_PACK, FR_ALPHA
   - FR_WINCAP_LONE, FR_WINCAP_PACK, FR_WINCAP_ALPHA
   - AD_REELS, AD_WINCAP

## Event Format (pour ELI)

Tous les events doivent emettre un dict avec:
```python
{
    "type": "eventName",
    "data": { ... }
}
```

Voir `docs/INTEGRATION_CONTRACT.md` pour les interfaces exactes.

## Commandes

```bash
# Run simulations
python run.py --mode PACK --sims 500000

# Optimize RTP
python run.py --optimize

# Generate configs
python run.py --export-config
```

## Tests
- RTP doit etre dans +/-0.1% de target
- Hit rate base: ~25-30%
- Free spin trigger: ~1/120-150
- Max win achievable sur 10M sims
