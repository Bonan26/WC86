// WC86 - Wolf Club 86 Asset Manifest

const assets = {
	// Fonts
	fonts: [
		{ alias: 'gold', src: 'fonts/goldFont/gold.fnt' },
		{ alias: 'alpha', src: 'fonts/alphaFont/alpha.fnt' },
	],

	// Sprite sheets
	spriteSheets: [
		'sprites/symbolsStatic/symbols.json',
		'sprites/uiAssets/ui.json',
		'sprites/reelsFrame/frame.json',
		'sprites/freeSpins/freespins.json',
		'sprites/progressBar/progressbar.json',
		'sprites/pressToContinueText/press.json',
	],

	// Spine animations - Symbols
	spines: [
		// Premium Wolves
		{ alias: 'boss_wolf', src: 'spines/symbols/boss_wolf/boss_wolf.json' },
		{ alias: 'hustler', src: 'spines/symbols/hustler/hustler.json' },
		{ alias: 'tech_bro', src: 'spines/symbols/tech_bro/tech_bro.json' },
		{ alias: 'diamond_hands', src: 'spines/symbols/diamond_hands/diamond_hands.json' },

		// Low Symbols (Club items)
		{ alias: 'cocktail', src: 'spines/symbols/cocktail/cocktail.json' },
		{ alias: 'vip_card', src: 'spines/symbols/vip_card/vip_card.json' },
		{ alias: 'disco_ball', src: 'spines/symbols/disco_ball/disco_ball.json' },
		{ alias: 'dice', src: 'spines/symbols/dice/dice.json' },

		// Special Symbols
		{ alias: 'alpha_wolf', src: 'spines/symbols/alpha_wolf/alpha_wolf.json' },
		{ alias: 'howling_wild', src: 'spines/symbols/howling_wild/howling_wild.json' },
		{ alias: 'moon_scatter', src: 'spines/symbols/moon_scatter/moon_scatter.json' },
		{ alias: 'territory', src: 'spines/symbols/territory/territory.json' },

		// Effects
		{ alias: 'huntMultiplier', src: 'spines/effects/huntMultiplier/huntMultiplier.json' },
		{ alias: 'howlChain', src: 'spines/effects/howlChain/howlChain.json' },
		{ alias: 'packSplit', src: 'spines/effects/packSplit/packSplit.json' },
		{ alias: 'territoryExpand', src: 'spines/effects/territoryExpand/territoryExpand.json' },
		{ alias: 'alphaDomination', src: 'spines/effects/alphaDomination/alphaDomination.json' },
		{ alias: 'bigwin', src: 'spines/effects/bigwin/bigwin.json' },
		{ alias: 'transition', src: 'spines/effects/transition/transition.json' },
		{ alias: 'anticipation', src: 'spines/effects/anticipation/anticipation.json' },
		{ alias: 'explosion', src: 'spines/effects/explosion/explosion.json' },

		// Backgrounds
		{ alias: 'backgroundBase', src: 'spines/backgrounds/base/base.json' },
		{ alias: 'backgroundPackHunt', src: 'spines/backgrounds/packHunt/packHunt.json' },
		{ alias: 'backgroundAlphaDomination', src: 'spines/backgrounds/alphaDomination/alphaDomination.json' },

		// UI
		{ alias: 'reelhouse', src: 'spines/ui/reelhouse/reelhouse.json' },
		{ alias: 'loader', src: 'spines/ui/loader/loader.json' },
		{ alias: 'fsIntro', src: 'spines/ui/fsIntro/fsIntro.json' },
		{ alias: 'fsIntroNumber', src: 'spines/ui/fsIntroNumber/fsIntroNumber.json' },
		{ alias: 'fsOutroNumber', src: 'spines/ui/fsOutroNumber/fsOutroNumber.json' },
	],

	// Audio
	audio: {
		src: 'audio/sounds.mp3',
		sprites: 'audio/sounds.json',
	},
};

export default assets;
