<script lang="ts">
	import { Rectangle, SpineProvider, SpineTrack } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../../game/context';

	const context = getContext();
	const backgroundProps = $derived(
		context.stateLayoutDerived.normalBackgroundLayout({ scale: 0.5 }),
	);

	// WC86: Nightclub theme - base game vs free game (Pack Hunt) vs Alpha Domination
	const showBaseBackground = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureBackground = $derived(context.stateGame.gameType === 'freegame');
	const showAlphaDominationBackground = $derived(context.stateGame.gameType === 'alphaDomination');
</script>

<!-- Black backdrop -->
<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x0a0a14} zIndex={-3} />

<!-- Base Game Background - Nightclub entrance -->
<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}>
	<SpineProvider key="backgroundBase" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'idle'} loop />
	</SpineProvider>
	<SpineProvider key="backgroundBase" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'neon_lights'} loop />
	</SpineProvider>
</FadeContainer>

<!-- Free Game Background - Inside the club (Pack Hunt) -->
<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}>
	<SpineProvider key="backgroundPackHunt" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'idle'} loop />
	</SpineProvider>
	<SpineProvider key="backgroundPackHunt" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'disco_lights'} loop />
	</SpineProvider>
</FadeContainer>

<!-- Alpha Domination Background - VIP area -->
<FadeContainer show={showAlphaDominationBackground} duration={SECOND} zIndex={-1}>
	<SpineProvider key="backgroundAlphaDomination" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'idle'} loop />
	</SpineProvider>
	<SpineProvider key="backgroundAlphaDomination" {...backgroundProps}>
		<SpineTrack trackIndex={0} animationName={'vip_lights'} loop />
	</SpineProvider>
</FadeContainer>
