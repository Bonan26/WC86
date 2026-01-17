<script lang="ts" module>
	import type { HowlChainData } from '../../game/types';

	export type EmitterEventHowlChain =
		| { type: 'howlChainAnimate'; data: HowlChainData }
		| { type: 'howlChainHide' };
</script>

<script lang="ts">
	import { SpineProvider, SpineTrack, BitmapText, Container, Graphics } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE, REEL_PADDING } from '../../game/constants';
	import { getSymbolX, getSymbolY } from '../../game/utils';
	import type { Position } from '../../game/types';

	const context = getContext();

	let visible = $state(false);
	let chainData = $state<HowlChainData | null>(null);
	let animation = $state<'chain_2' | 'chain_3plus' | 'connection'>('chain_2');

	context.eventEmitter.subscribeOnMount({
		howlChainAnimate: async ({ data }) => {
			chainData = data;
			visible = true;

			// Choose animation based on chain type
			animation = data.chainType === 'additive' ? 'chain_2' : 'chain_3plus';

			// Auto-hide after animation
			await waitForTimeout(1500);
			visible = false;
		},
		howlChainHide: () => {
			visible = false;
			chainData = null;
		},
	});

	// Calculate position for the chain multiplier display
	const chainPosition = $derived.by(() => {
		if (!chainData || chainData.wildPositions.length === 0) {
			return { x: 0, y: 0 };
		}

		// Center the display between the wild positions
		const avgX = chainData.wildPositions.reduce((sum, pos) => sum + getSymbolX(pos.reel), 0) / chainData.wildPositions.length;
		const avgY = chainData.wildPositions.reduce((sum, pos) => sum + getSymbolY(pos.row), 0) / chainData.wildPositions.length;

		return {
			x: context.stateGameDerived.boardLayout().x - context.stateGameDerived.boardLayout().width / 2 + avgX,
			y: context.stateGameDerived.boardLayout().y - context.stateGameDerived.boardLayout().height / 2 + avgY - SYMBOL_SIZE * 0.5,
		};
	});
</script>

<MainContainer>
	<FadeContainer show={visible}>
		{#if chainData}
			<!-- Draw connection lines between wilds -->
			<Container
				x={context.stateGameDerived.boardLayout().x - context.stateGameDerived.boardLayout().width / 2}
				y={context.stateGameDerived.boardLayout().y - context.stateGameDerived.boardLayout().height / 2}
			>
				<!-- Connection effect animation -->
				{#each chainData.wildPositions as wildPos, index}
					{#if index < chainData.wildPositions.length - 1}
						{@const nextPos = chainData.wildPositions[index + 1]}
						<SpineProvider
							key="howlChain"
							x={(getSymbolX(wildPos.reel) + getSymbolX(nextPos.reel)) / 2}
							y={(getSymbolY(wildPos.row) + getSymbolY(nextPos.row)) / 2}
							width={SYMBOL_SIZE * 0.5}
						>
							<SpineTrack
								trackIndex={0}
								animationName="connection"
								loop={false}
							/>
						</SpineProvider>
					{/if}

					<!-- Individual wild multiplier display -->
					<BitmapText
						anchor={0.5}
						x={getSymbolX(wildPos.reel)}
						y={getSymbolY(wildPos.row) - SYMBOL_SIZE * 0.4}
						text={`x${wildPos.multiplier}`}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.3,
						}}
					/>
				{/each}
			</Container>

			<!-- Chain multiplier result -->
			<Container {...chainPosition}>
				<SpineProvider key="howlChainResult" width={SYMBOL_SIZE * 2}>
					<SpineTrack
						trackIndex={0}
						animationName={animation}
						loop={false}
					/>
				</SpineProvider>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.3}
					text={chainData.chainType === 'additive' ? `+${chainData.chainMultiplier}x` : `x${chainData.chainMultiplier}`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.6,
						fontWeight: 'bold',
					}}
				/>

				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.7}
					text={chainData.chainType === 'additive' ? 'ADDITIVE' : 'MULTIPLICATIVE'}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.2,
					}}
				/>
			</Container>
		{/if}
	</FadeContainer>
</MainContainer>
