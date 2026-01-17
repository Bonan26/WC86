# WC86 - Wolf Club 86 - Assets

## Context pour Claude (ARIE)
Tu travailles sur les **Assets** du jeu WC86 - Wolf Club 86. Theme: Nightclub retro 80s avec des loups. Ce README te donne tout le contexte necessaire.

## Outil: Nano Banana API
Utilise l'API Nano Banana pour generer les assets.

## Structure requise

```
assets/
├── audio/
│   ├── sounds.mp3          # Audio sprite (tous les sons)
│   └── sounds.json         # Config des sprites
├── fonts/
│   ├── alphaFont/          # Police principale style wolf
│   ├── goldFont/           # Police pour wins
│   └── cryptoFont/         # Police pour crypto symbols
├── spines/
│   ├── symbols/            # 12 symboles
│   └── effects/            # 8 effets
└── sprites/
    ├── symbolsStatic/      # 12 PNG
    └── ...                 # 5 autres dossiers
```

## Audio (60 sprites)

### Format
- sounds.mp3: Audio sprite unique
- sounds.json: Config format Howler.js

### sounds.json structure
```json
{
  "src": ["sounds.mp3"],
  "sprite": {
    "bgm_main": [0, 120000, true],
    "bgm_freespin": [120000, 90000, true],
    "bgm_alpha_domination": [210000, 60000, true],
    "sfx_spin_start": [270000, 500],
    "sfx_reel_stop": [270500, 200],
    "sfx_cascade_explosion": [270700, 400]
  }
}
```

### Liste des 60 sprites audio

**BGM (3):**
1. bgm_main - 2min loop, lo-fi chill
2. bgm_freespin - 1.5min loop, synthwave
3. bgm_alpha_domination - 1min loop, epic

**SFX Spins (8):**
4-9. sfx_reel_stop_1 → sfx_reel_stop_6
10. sfx_spin_start
11. sfx_anticipation

**SFX Scatter (7):**
12-17. sfx_scatter_stop_1 → sfx_scatter_stop_6
18. sfx_scatter_win

**SFX Wins (10):**
19. sfx_win_small
20. sfx_win_medium
21. sfx_win_large
22-26. tumble_win_1 → tumble_win_5
27. sfx_bigwin_coinloop
28. sfx_youwon_panel

**SFX Features (20):**
29. sfx_multiplier_up
30. sfx_multiplier_max
31. sfx_pack_split
32. sfx_howl_chain_add
33. sfx_howl_chain_multi
34. sfx_territory_expand
35. sfx_freespin_trigger
36. sfx_freespin_intro
37. sfx_freespin_retrigger
38. sfx_alpha_domination_intro
39. sfx_wolf_howl_1
40. sfx_wolf_howl_2
41. sfx_cascade_explosion
42. sfx_symbols_landing
... (et autres)

**SFX UI (10):**
50. sfx_btn_general
51. sfx_btn_spin
52. sfx_menu_open
... (et autres)

## Spines (20 dossiers)

### Format par dossier
```
symbol_name/
├── symbol_name.atlas
├── symbol_name.json
└── symbol_name.png
```

### Symboles (12 dossiers)

| Symbole | Animations requises | Style |
|---------|---------------------|-------|
| boss_wolf | idle, land, win, explosion | Alpha wolf, corporate suit, dominant |
| hustler | idle, land, win, explosion | Streetwear wolf, chains, confident |
| tech_bro | idle, land, win, explosion | Hoodie wolf, laptop, glasses |
| diamond_hands | idle, land, win, explosion | Wolf with diamond paws, hodl pose |
| cocktail | idle, land, win, explosion | Martini neon style 80s, glowing |
| vip_card | idle, land, win, explosion | Carte membre doree, premium |
| disco_ball | idle, land, win, explosion | Boule disco brillante, reflective |
| dice | idle, land, win, explosion | Des lumineux neon, fun |
| alpha_wolf | idle, land, win, explosion, **split** | Leader wolf, red eyes, powerful |
| howling_wild | idle, land, win, explosion, **howl** | Wolf howling at moon, multiplier |
| moon_scatter | idle, land, win, explosion | Full moon, scatter text |
| territory | idle, land, win, explosion, **glow** | Territory marker, golden |

### Effets (8 dossiers)

| Effet | Animations | Description |
|-------|------------|-------------|
| huntMultiplier | idle, increase, maxed | Compteur x1-x500 |
| howlChain | chain_2, chain_3plus, connection | Lignes entre wilds |
| packSplit | split, duplicate | Duplication effect |
| territoryExpand | expand_7x6, expand_8x7, expand_8x8 | Grid expansion |
| alphaDomination | intro, idle, outro | Super bonus animations |
| bigwin | big, super, mega, epic, max | Win celebrations |
| transition | base_to_fs, fs_to_base | Scene transitions |
| anticipation | reel_glow | Anticipation sur reels |

## Sprites (6 dossiers)

### symbolsStatic/ (12 PNG)
Format: 200x200 PNG, transparent background
- boss_wolf.png
- hustler.png
- tech_bro.png
- diamond_hands.png
- cocktail.png
- vip_card.png
- disco_ball.png
- dice.png
- alpha_wolf.png
- howling_wild.png
- moon_scatter.png
- territory.png

### reelsFrame/
- frame_6x5.png
- frame_7x6.png
- frame_8x7.png
- frame_8x8.png
- frame_glow.png

### freeSpins/
- fs_background.png
- fs_frame.png
- fs_counter_bg.png

### progressBar/
- progress_bar_bg.png
- progress_bar_fill.png
- territory_icon.png

### pressToContinueText/
- press_continue_en.png
- press_continue_fr.png

### uiAssets/
- logo.png
- buy_bonus_btn.png
- volatility_lone.png
- volatility_pack.png
- volatility_alpha.png

## Fonts (3 dossiers)

### alphaFont/
Police principale du jeu. Style: Bold, wolf-themed, angular.
- alphaFont.fnt
- alphaFont.png

### goldFont/
Police pour afficher les wins. Style: Gold, shiny, celebratory.
- goldFont.fnt
- goldFont.png

### cryptoFont/
Police pour les montants crypto. Style: Modern, digital, clean.
- cryptoFont.fnt
- cryptoFont.png

## Nommage (IMPORTANT)

STEPH attend ces noms exacts pour ses composants:
```typescript
// Spines
'spines/symbols/boss_wolf/boss_wolf'
'spines/effects/huntMultiplier/huntMultiplier'

// Sprites
'sprites/symbolsStatic/boss_wolf.png'

// Audio
'audio/sounds' // loads sounds.mp3 + sounds.json

// Fonts
'fonts/alphaFont/alphaFont'
```

## Checklist

### Audio
- [ ] sounds.mp3 genere avec tous les sprites
- [ ] sounds.json avec timings corrects
- [ ] Volume normalise
- [ ] Loops seamless pour BGM

### Spines
- [ ] 12 symboles avec 4-5 animations chacun
- [ ] 8 effets avec animations listees
- [ ] Toutes les animations testees
- [ ] Tailles optimisees

### Sprites
- [ ] 12 PNG symboles 200x200
- [ ] 4 frames grille
- [ ] UI assets complets
- [ ] Transparent backgrounds

### Fonts
- [ ] 3 fonts avec tous les caracteres necessaires
- [ ] Format .fnt + .png