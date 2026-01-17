# WC86 - Wolf Club 86

## Overview
Slot haute volatilite 6x5→8x8 avec mecaniques avancees. Theme: Nightclub retro 80s avec des loups.

**Caracteristiques:**
- Grille dynamique: 6x5 (7,776 ways) → 8x8 (262,144 ways)
- 3 modes de volatilite: LONE_WOLF (96.8%), PACK (96.5%), ALPHA (96.2%)
- Max wins: 10,000x / 25,000x / 50,000x
- 4 bet modes: base, pack_hunt (75x), pack_hunt_plus (150x), alpha_domination (500x)

## Team

| Dev | Role | Scope | Branch |
|-----|------|-------|--------|
| **DAN** | Math Engine | Math-SDK complet (Python + Rust) | `feature/math-sdk` |
| **ELI** | Web Core | Web-SDK game/ + state + events | `feature/web-core` |
| **STEPH** | Web Components | Web-SDK components/ + animations | `feature/web-components` |
| **ARIE** | Assets | Tous les assets (Nano Banana API) | `feature/assets` |

## Quick Start

```bash
# Math SDK
cd math-sdk/games/wc86
python run.py

# Web SDK
cd web-sdk/apps/wc86
npm install && npm run dev
```

## Documentation

- [Plan d'implementation](WC86_Implementation_Plan.md) - Reference complete
- [Contrat d'integration](docs/INTEGRATION_CONTRACT.md) - Interfaces entre devs

## Structure

```
WC86/
├── math-sdk/games/wc86/            # DAN - Python + Rust
├── web-sdk/apps/wc86/
│   ├── src/game/                   # ELI - TypeScript
│   ├── src/components/             # STEPH - Svelte
│   └── static/assets/              # ARIE - Assets
└── docs/                           # Documentation partagee
```

## Symboles (12)

**Premium (Wolves):**
- BOSS_WOLF - Le patron du club
- HUSTLER - Le loup streetwear
- TECH_BRO - Le loup geek
- DIAMOND_HANDS - Le loup high roller

**Low (Club items):**
- COCKTAIL - Martini neon
- VIP_CARD - Carte membre doree
- DISCO_BALL - Boule disco
- DICE - Des lumineux

**Special:**
- ALPHA_WOLF - Wild, Pack Split
- HOWLING_WILD - Wild avec multiplicateur
- MOON_SCATTER - Scatter Free Spins
- TERRITORY - Expansion de grille

## Milestones

- [ ] M1: Math Core - Simulations 100k fonctionnelles (DAN)
- [ ] M2: Web Skeleton - App demarre, state machine OK (ELI)
- [ ] M3: Basic Spin - Spin basique avec symboles statiques (ELI + STEPH)
- [ ] M4: Assets V1 - Symboles statiques + 1 animation (ARIE)
- [ ] M5: Cascade - Hunt Cascade fonctionnel (ALL)
- [ ] M6: Features - Pack Split, Howl Chain, Territory (ALL)
- [ ] M7: Free Spins - Pack Hunt complet (ALL)
- [ ] M8: Polish - Alpha Domination + audio + polish (ALL)
- [ ] M9: QA - Tests complets, RTP valide (ALL)

## Workflow GitHub

### Branches
```
main
├── develop                      # Integration branch
├── feature/math-sdk            # DAN
├── feature/web-core            # ELI
├── feature/web-components      # STEPH
└── feature/assets              # ARIE
```

### Regles
1. Chaque dev travaille sur sa branch
2. PR vers `develop` quand feature complete
3. Review obligatoire par 1 autre dev
4. Merge `develop` → `main` quand milestone atteint

## Communication

### Standup format (async)
```
**[NOM] - [DATE]**
Done: ...
Today: ...
Blockers: ...
```
