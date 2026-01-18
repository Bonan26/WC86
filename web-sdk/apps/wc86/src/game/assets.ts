// WC86 - Wolf Club 86 Asset Manifest

export default {
	// ============ FONTS ============
	gold: {
		type: 'font',
		src: new URL('../../assets/fonts/goldFont/gold.xml', import.meta.url).href,
	},
	alpha: {
		type: 'font',
		src: new URL('../../assets/fonts/alphaFont/alpha.xml', import.meta.url).href,
	},

	// ============ SPRITE SHEETS ============
	symbolsStatic: {
		type: 'sprites',
		src: new URL('../../assets/sprites/symbolsStatic/symbols.json', import.meta.url).href,
	},
	uiAssets: {
		type: 'sprites',
		src: new URL('../../assets/sprites/uiAssets/ui.json', import.meta.url).href,
	},
	reelsFrame: {
		type: 'sprites',
		src: new URL('../../assets/sprites/reelsFrame/frame.json', import.meta.url).href,
	},
	freeSpins: {
		type: 'sprites',
		src: new URL('../../assets/sprites/freeSpins/freespins.json', import.meta.url).href,
	},
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressbar.json', import.meta.url).href,
		preload: true,
	},
	pressToContinueText: {
		type: 'sprites',
		src: new URL('../../assets/sprites/pressToContinueText/press.json', import.meta.url).href,
		preload: true,
	},

	// ============ SPINE SYMBOLS - Premium Wolves ============
	boss_wolf: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/boss_wolf/boss_wolf.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/boss_wolf/boss_wolf.json', import.meta.url).href,
			scale: 2,
		},
	},
	hustler: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/hustler/hustler.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/hustler/hustler.json', import.meta.url).href,
			scale: 2,
		},
	},
	tech_bro: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/tech_bro/tech_bro.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/tech_bro/tech_bro.json', import.meta.url).href,
			scale: 2,
		},
	},
	diamond_hands: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/diamond_hands/diamond_hands.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/diamond_hands/diamond_hands.json', import.meta.url).href,
			scale: 2,
		},
	},

	// ============ SPINE SYMBOLS - Low (Club items) ============
	cocktail: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/cocktail/cocktail.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/cocktail/cocktail.json', import.meta.url).href,
			scale: 2,
		},
	},
	vip_card: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/vip_card/vip_card.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/vip_card/vip_card.json', import.meta.url).href,
			scale: 2,
		},
	},
	disco_ball: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/disco_ball/disco_ball.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/disco_ball/disco_ball.json', import.meta.url).href,
			scale: 2,
		},
	},
	dice: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/dice/dice.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/dice/dice.json', import.meta.url).href,
			scale: 2,
		},
	},

	// ============ SPINE SYMBOLS - Special ============
	alpha_wolf: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/alpha_wolf/alpha_wolf.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/alpha_wolf/alpha_wolf.json', import.meta.url).href,
			scale: 2,
		},
	},
	howling_wild: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/howling_wild/howling_wild.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/howling_wild/howling_wild.json', import.meta.url).href,
			scale: 2,
		},
	},
	moon_scatter: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/moon_scatter/moon_scatter.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/moon_scatter/moon_scatter.json', import.meta.url).href,
			scale: 2,
		},
	},
	territory: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols/territory/territory.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols/territory/territory.json', import.meta.url).href,
			scale: 2,
		},
	},

	// ============ SPINE EFFECTS ============
	huntMultiplier: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/huntMultiplier/huntMultiplier.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/huntMultiplier/huntMultiplier.json', import.meta.url).href,
			scale: 2,
		},
	},
	howlChain: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/howlChain/howlChain.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/howlChain/howlChain.json', import.meta.url).href,
			scale: 2,
		},
	},
	packSplit: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/packSplit/packSplit.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/packSplit/packSplit.json', import.meta.url).href,
			scale: 2,
		},
	},
	territoryExpand: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/territoryExpand/territoryExpand.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/territoryExpand/territoryExpand.json', import.meta.url).href,
			scale: 2,
		},
	},
	alphaDomination: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/alphaDomination/alphaDomination.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/alphaDomination/alphaDomination.json', import.meta.url).href,
			scale: 2,
		},
	},
	bigwin: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/bigwin/bigwin.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/bigwin/bigwin.json', import.meta.url).href,
			scale: 2,
		},
	},
	transition: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/transition/transition.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/transition/transition.json', import.meta.url).href,
			scale: 2,
		},
	},
	anticipation: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/anticipation/anticipation.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/anticipation/anticipation.json', import.meta.url).href,
			scale: 2,
		},
	},
	explosion: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/effects/explosion/explosion.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/effects/explosion/explosion.json', import.meta.url).href,
			scale: 2,
		},
	},

	// ============ SPINE BACKGROUNDS ============
	backgroundBase: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/backgrounds/base/base.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/backgrounds/base/base.json', import.meta.url).href,
			scale: 2,
		},
		preload: true,
	},
	backgroundPackHunt: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/backgrounds/packHunt/packHunt.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/backgrounds/packHunt/packHunt.json', import.meta.url).href,
			scale: 2,
		},
		preload: true,
	},
	backgroundAlphaDomination: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/backgrounds/alphaDomination/alphaDomination.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/backgrounds/alphaDomination/alphaDomination.json', import.meta.url).href,
			scale: 2,
		},
		preload: true,
	},

	// ============ SPINE UI ============
	reelhouse: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/ui/reelhouse/reelhouse.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/ui/reelhouse/reelhouse.json', import.meta.url).href,
			scale: 2,
		},
	},
	loader: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/ui/loader/loader.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/ui/loader/loader.json', import.meta.url).href,
			scale: 2,
		},
		preload: true,
	},
	fsIntro: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/ui/fsIntro/fsIntro.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/ui/fsIntro/fsIntro.json', import.meta.url).href,
			scale: 2,
		},
	},
	fsIntroNumber: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/ui/fsIntro/fsIntro.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/ui/fsIntroNumber/fsIntroNumber.json', import.meta.url).href,
			scale: 2,
		},
	},
	fsOutroNumber: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/ui/fsIntro/fsIntro.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/ui/fsOutroNumber/fsOutroNumber.json', import.meta.url).href,
			scale: 2,
		},
	},

	// ============ AUDIO ============
	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;
