<script lang="ts" module>
	import type { PackSplitData } from '../../game/types';

	export type EmitterEventPackSplit =
		| { type: 'packSplitAnimate'; data: PackSplitData }
		| { type: 'packSplitHide' };
</script>

<script lang="ts">
	import { SpineProvider, SpineTrack, BitmapText, Container } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE } from '../../game/constants';
	import { getSymbolX, getSymbolY } from '../../game/utils';

	const context = getContext();

	let visible = $state(false);
	let splitData = $state<PackSplitData | null>(null);
	let animationPhase = $state<'split' | 'duplicate' | 'complete'>('split');

	context.eventEmitter.subscribeOnMount({
		packSplitAnimate: async ({ data }) => {
			splitData = data;
			visible = true;
			animationPhase = 'split';

			// Split animation phase
			await waitForTimeout(400);
			animationPhase = 'duplicate';

			// Duplicate animation phase
			await waitForTimeout(600);
			animationPhase = 'complete';

			// Hide after animation
			await waitForTimeout(300);
			visible = false;
		},
		packSplitHide: () => {
			visible = false;
			splitData = null;
		},
	});

	// Calculate alpha wolf position on screen
	const alphaPosition = $derived.by(() => {
		if (!splitData) return { x: 0, y: 0 };

		return {
			x: context.stateGameDerived.boardLayout().x -
				context.stateGameDerived.boardLayout().width / 2 +
				getSymbolX(splitData.alphaPosition.reel),
			y: context.stateGameDerived.boardLayout().y -
				context.stateGameDerived.boardLayout().height / 2 +
				getSymbolY(splitData.alphaPosition.row),
		};
	});
</script>

<MainContainer>
	<FadeContainer show={visible}>
		{#if splitData}
			<!-- Alpha Wolf Split Animation -->
			<Container {...alphaPosition}>
				<SpineProvider key="alpha_wolf" width={SYMBOL_SIZE * 1.2}>
					<SpineTrack
						trackIndex={0}
						animationName={animationPhase === 'split' ? 'split' : 'win'}
						loop={false}
					/>
				</SpineProvider>
			</Container>

			<!-- Duplicated positions animation -->
			{#if animationPhase === 'duplicate' || animationPhase === 'complete'}
				{#each splitData.affectedPositions as pos, index}
					{@const targetX = context.stateGameDerived.boardLayout().x -
						context.stateGameDerived.boardLayout().width / 2 +
						getSymbolX(pos.reel)}
					{@const targetY = context.stateGameDerived.boardLayout().y -
						context.stateGameDerived.boardLayout().height / 2 +
						getSymbolY(pos.row)}

					<Container x={targetX} y={targetY}>
						<SpineProvider key="packSplit" width={SYMBOL_SIZE}>
							<SpineTrack
								trackIndex={0}
								animationName="duplicate"
								loop={false}
							/>
						</SpineProvider>
					</Container>
				{/each}
			{/if}

			<!-- Split multiplier display -->
			<Container
				x={context.stateGameDerived.boardLayout().x}
				y={context.stateGameDerived.boardLayout().y - context.stateGameDerived.boardLayout().height * 0.5 - SYMBOL_SIZE}
			>
				<SpineProvider key="packSplitMultiplier" width={SYMBOL_SIZE * 2}>
					<SpineTrack
						trackIndex={0}
						animationName="multiplier_reveal"
						loop={false}
					/>
				</SpineProvider>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.2}
					text={`PACK SPLIT x${splitData.cumulativeMultiplier}`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.4,
						fontWeight: 'bold',
					}}
				/>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.6}
					text={`${splitData.splitCount} DUPLICATES`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.25,
					}}
				/>
			</Container>
		{/if}
	</FadeContainer>
</MainContainer>
