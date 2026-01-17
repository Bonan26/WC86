<script lang="ts" module>
	export type EmitterEventSound =
		| { type: 'soundOnce'; name: string; forcePlay?: boolean }
		| { type: 'soundScatterCounterIncrease' }
		| { type: 'soundBgmSwitch'; bgm: 'base' | 'freegame' | 'alphaDomination' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { getContext } from '../../game/context';

	const context = getContext();

	// Sound effect mappings for WC86
	const sfxNames = {
		// Reel sounds
		sfx_spin_start: 'sfx_spin_start',
		sfx_reel_stop: 'sfx_reel_stop',

		// Symbol sounds
		sfx_alpha_wolf_land: 'sfx_alpha_wolf_land',
		sfx_howling_wild_land: 'sfx_howling_wild_land',
		sfx_wild_explode: 'sfx_wild_explode',
		sfx_howl: 'sfx_howl',

		// Scatter sounds
		sfx_scatter_land_1: 'sfx_scatter_land_1',
		sfx_scatter_land_2: 'sfx_scatter_land_2',
		sfx_scatter_land_3: 'sfx_scatter_land_3',
		sfx_scatter_land_4: 'sfx_scatter_land_4',
		sfx_scatter_land_5: 'sfx_scatter_land_5',
		sfx_scatter_land_6: 'sfx_scatter_land_6',

		// Territory sounds
		sfx_territory_land_1: 'sfx_territory_land_1',
		sfx_territory_land_2: 'sfx_territory_land_2',
		sfx_territory_land_3: 'sfx_territory_land_3',
		sfx_territory_expand: 'sfx_territory_expand',

		// Feature sounds
		sfx_multiplier_increase: 'sfx_multiplier_increase',
		sfx_pack_split: 'sfx_pack_split',
		sfx_howl_chain_add: 'sfx_howl_chain_add',
		sfx_howl_chain_multi: 'sfx_howl_chain_multi',
		sfx_freespin_trigger: 'sfx_freespin_trigger',
		sfx_freespin_retrigger: 'sfx_freespin_retrigger',
		sfx_alpha_domination_intro: 'sfx_alpha_domination_intro',

		// Win sounds
		sfx_win_small: 'sfx_win_small',
		sfx_win_big: 'sfx_win_big',
		sfx_win_mega: 'sfx_win_mega',
		sfx_win_epic: 'sfx_win_epic',
		sfx_win_max: 'sfx_win_max',
	};

	// BGM tracks
	const bgmTracks = {
		base: 'bgm_main',
		freegame: 'bgm_pack_hunt',
		alphaDomination: 'bgm_alpha_domination',
	};

	let currentBgm = $state<string | null>(null);

	context.eventEmitter.subscribeOnMount({
		soundOnce: ({ name, forcePlay }) => {
			// Sound playback would be handled by the sound system
			console.log('Play sound:', name, forcePlay ? '(forced)' : '');
		},
		soundScatterCounterIncrease: () => {
			console.log('Scatter counter increased');
		},
		soundBgmSwitch: ({ bgm }) => {
			const newBgm = bgmTracks[bgm];
			if (currentBgm !== newBgm) {
				currentBgm = newBgm;
				console.log('Switch BGM to:', newBgm);
			}
		},
	});

	onMount(() => {
		// Start with base game BGM
		currentBgm = bgmTracks.base;
	});
</script>
