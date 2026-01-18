<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Text, REM } from 'pixi-svelte';
	import { stateModal } from 'state-shared';

	import { UI, UiGameName } from 'components-ui-pixi';
	import { GameVersion, Modals } from 'components-ui-html';

	import { getContext } from '../../game/context';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import BoardFrame from './BoardFrame.svelte';
	import Board from './Board.svelte';
	import Win from './Win.svelte';
	import FreeSpinIntro from './FreeSpinIntro.svelte';
	import FreeSpinCounter from './FreeSpinCounter.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';

	// WC86 Custom Components
	import HuntMultiplier from '../custom/HuntMultiplier.svelte';
	import TerritoryExpand from '../custom/TerritoryExpand.svelte';
	import HowlChainEffect from '../custom/HowlChainEffect.svelte';
	import PackSplitAnimation from '../custom/PackSplitAnimation.svelte';
	import GridExpansion from '../custom/GridExpansion.svelte';
	import AlphaDominationIntro from '../custom/AlphaDominationIntro.svelte';
	import VolatilitySelector from '../custom/VolatilitySelector.svelte';

	const context = getContext();

	onMount(() => (context.stateLayout.showLoadingScreen = true));

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
	});
</script>

<App>
	<EnableSound />
	<EnableHotkey />
	<EnableGameActor />
	<EnablePixiExtension />

	<Background />

	{#if context.stateLayout.showLoadingScreen}
		<LoadingScreen onloaded={() => (context.stateLayout.showLoadingScreen = false)} />
	{:else}
		<ResumeBet />
		<!--
			The reason why <Sound /> is rendered after clicking the loading screen:
			"Autoplay with sound is allowed if: The user has interacted with the domain (click, tap, etc.)."
			Ref: https://developer.chrome.com/blog/autoplay
		-->
		<Sound />

		<MainContainer>
			<BoardFrame />
		</MainContainer>

		<MainContainer>
			<Board />
		</MainContainer>

		<!-- WC86 Hunt Multiplier Display -->
		<HuntMultiplier />

		<!-- Territory Progress -->
		<TerritoryExpand />

		<!-- Pack Split Animation -->
		<PackSplitAnimation />

		<!-- Howl Chain Effect -->
		<HowlChainEffect />

		<!-- Grid Expansion Animation -->
		<GridExpansion />

		<!-- Alpha Domination Intro -->
		<AlphaDominationIntro />

		<!-- Volatility Selector (shown at game start) -->
		<VolatilitySelector />

		<UI>
			{#snippet gameName()}
				<UiGameName name="WOLF CLUB 86" />
			{/snippet}
			{#snippet logo()}
				<Text
					anchor={{ x: 1, y: 0 }}
					text="WC86"
					style={{
						fontFamily: 'proxima-nova',
						fontSize: REM * 1.5,
						fontWeight: '600',
						lineHeight: REM * 2,
						fill: 0xff00ff,
					}}
				/>
			{/snippet}
		</UI>
		<Win />
		<FreeSpinIntro />
		{#if ['desktop', 'landscape'].includes(context.stateLayoutDerived.layoutType())}
			<FreeSpinCounter />
		{/if}
		<FreeSpinOutro />
		<Transition />
	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="1.0.0" />
	{/snippet}
</Modals>
