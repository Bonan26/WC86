# WC86 - Prompts Initiaux pour l'Équipe

Chaque dev copie son prompt et le donne à Claude Code pour démarrer.

---

## DAN - Math Engine

```
Je suis DAN, je travaille sur le Math-SDK du jeu WC86 (Wolf Club 86).

Lis d'abord ces fichiers pour le contexte:
1. /math-sdk/games/wc86/README.md (mon scope)
2. /docs/INTEGRATION_CONTRACT.md (interfaces avec ELI)

Ma tâche: Créer le math engine complet en Python.

Commence par créer game_config.py avec:
- Les 12 symboles (4 wolves premium, 4 club items, 4 special)
- La paytable complète
- Les 3 modes de volatilité (LONE_WOLF, PACK, ALPHA)
- Les 4 bet modes

Respecte le format des Book Events défini dans le contrat pour que ELI puisse les consommer.
```

---

## ELI - Web Core

```
Je suis ELI, je travaille sur le Web Core du jeu WC86 (Wolf Club 86).

Lis d'abord ces fichiers pour le contexte:
1. /web-sdk/apps/wc86/README.md (mon scope)
2. /docs/INTEGRATION_CONTRACT.md (interfaces avec DAN et STEPH)

Ma tâche: Créer le state management et les event handlers en TypeScript/Svelte 5.

Commence par créer dans src/game/:
1. types.ts - Les types de base (SymbolName, GridConfig, etc.)
2. typesBookEvent.ts - Interfaces des events de DAN
3. stateGame.svelte.ts - État du jeu avec $state()

Je dois consommer les Book Events de DAN et émettre des Emitter Events pour STEPH.
```

---

## STEPH - Web Components

```
Je suis STEPH, je travaille sur les Components Svelte du jeu WC86 (Wolf Club 86).

Lis d'abord ces fichiers pour le contexte:
1. /web-sdk/apps/wc86/src/components/README.md (mon scope)
2. /docs/INTEGRATION_CONTRACT.md (interfaces avec ELI et ARIE)

Ma tâche: Créer les composants Svelte 5 + PixiJS pour les animations.

Commence par créer dans src/components/core/:
1. Game.svelte - Root component
2. Board.svelte - Container du board
3. Symbol.svelte - Wrapper pour afficher un symbole

J'écoute les Emitter Events de ELI et j'utilise les assets paths de ARIE.
Note: Utilise des placeholders en attendant les vrais assets.
```

---

## ARIE - Assets

```
Je suis ARIE, je travaille sur les Assets du jeu WC86 (Wolf Club 86).

Lis d'abord ces fichiers pour le contexte:
1. /web-sdk/apps/wc86/static/assets/README.md (mon scope)
2. /docs/INTEGRATION_CONTRACT.md (interfaces avec STEPH)

Ma tâche: Créer tous les assets visuels et audio.

J'ai déjà les wolf parts dans /Wolf_parts_final/ pour assembler les 4 loups premium.
Pour le reste (club items, effets, UI, audio), j'utilise Gemini.

Respecte les paths et noms d'animations définis dans le contrat pour que STEPH puisse les utiliser.
```

---

## Ordre de démarrage recommandé

1. **Tous en parallèle** - Chacun peut commencer immédiatement
2. **Premier sync** - Quand DAN a `game_config.py`, ELI peut valider les types
3. **Second sync** - Quand ARIE a les premiers assets, STEPH peut tester visuellement

## Fichiers de référence communs

- `/docs/INTEGRATION_CONTRACT.md` - Interfaces entre devs
- `/WC86_Implementation_Plan.md` - Plan complet
- `/README.md` - Vue d'ensemble du projet
