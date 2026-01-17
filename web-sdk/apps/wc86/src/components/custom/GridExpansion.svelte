<script lang="ts" module>
	import type { TerritoryExpandData } from '../../game/types';

	export type EmitterEventGridExpansion = { type: 'gridExpand'; data: TerritoryExpandData };
</script>

<script lang="ts">
	import { SpineProvider, SpineTrack, BitmapText, Container, Rectangle } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer, CanvasSizeRectangle } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE, GRID_CONFIGS } from '../../game/constants';
	import type { GridSize } from '../../game/types';

	const context = getContext();

	let visible = $state(false);
	let expandData = $state<TerritoryExpandData | null>(null);
	let animationPhase = $state<'intro' | 'expand' | 'complete'>('intro');

	// Animation name based on the new grid size
	const animationName = $derived.by(() => {
		if (!expandData) return 'expand_7x6';
		return `expand_${expandData.newGrid.replace('x', 'x')}`;
	});

	context.eventEmitter.subscribeOnMount({
		gridExpand: async ({ data }) => {
			expandData = data;
			visible = true;
			animationPhase = 'intro';

			// Intro phase
			await waitForTimeout(500);
			animationPhase = 'expand';

			// Expansion animation
			await waitForTimeout(1000);
			animationPhase = 'complete';

			// Auto-hide
			await waitForTimeout(500);
			visible = false;
		},
	});

	const position = $derived({
		x: context.stateGameDerived.boardLayout().x,
		y: context.stateGameDerived.boardLayout().y,
	});
</script>

{#if visible && expandData}
	<!-- Dark overlay -->
	<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.6} />

	<MainContainer>
		<Container {...position}>
			<!-- Grid expansion spine animation -->
			<SpineProvider key="territoryExpand" width={context.stateGameDerived.boardLayout().width * 1.2}>
				<SpineTrack
					trackIndex={0}
					animationName={animationName}
					loop={false}
				/>
			</SpineProvider>

			<!-- Expansion info display -->
			<Container y={-SYMBOL_SIZE * 2}>
				<BitmapText
					anchor={0.5}
					text="TERRITORY EXPANSION"
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.5,
						fontWeight: 'bold',
					}}
				/>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.6}
					text={`${expandData.previousGrid} → ${expandData.newGrid}`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.7,
						fontWeight: 'bold',
					}}
				/>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 1.3}
					text={`${GRID_CONFIGS[expandData.newGrid].ways.toLocaleString()} WAYS`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.35,
					}}
				/>
			</Container>
		</Container>
	</MainContainer>
{/if}
