<script lang="ts" module>
	import type { AlphaDominationStartData } from '../../game/typesBookEvent';

	export type EmitterEventAlphaDomination =
		| { type: 'alphaDominationIntroShow'; data: AlphaDominationStartData }
		| { type: 'alphaDominationIntroHide' };
</script>

<script lang="ts">
	import { SpineProvider, SpineTrack, BitmapText, Container, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer, CanvasSizeRectangle } from 'components-layout';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE, GRID_CONFIGS } from '../../game/constants';
	import PressToContinue from '../core/PressToContinue.svelte';
	import type { AlphaDominationStartData } from '../../game/typesBookEvent';

	const context = getContext();

	let visible = $state(false);
	let introData = $state<AlphaDominationStartData | null>(null);
	let animationPhase = $state<'intro' | 'idle' | 'outro'>('intro');
	let oncomplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		alphaDominationIntroShow: async ({ data }) => {
			introData = data;
			visible = true;
			animationPhase = 'intro';

			// Wait for user interaction
			await waitForResolve((resolve) => (oncomplete = resolve));

			animationPhase = 'outro';
			await waitForTimeout(500);
			visible = false;
		},
		alphaDominationIntroHide: () => {
			visible = false;
			introData = null;
		},
	});

	const position = $derived({
		x: context.stateGameDerived.boardLayout().x,
		y: context.stateGameDerived.boardLayout().y,
	});
</script>

<FadeContainer show={visible}>
	<!-- Full screen dark overlay with purple tint for VIP feel -->
	<CanvasSizeRectangle backgroundColor={0x1a0a2e} backgroundAlpha={0.9} />

	{#if introData}
		<MainContainer>
			<Container {...position}>
				<!-- Alpha Domination Spine Animation -->
				<SpineProvider key="alphaDomination" width={context.stateGameDerived.boardLayout().width * 1.5}>
					<SpineTrack
						trackIndex={0}
						animationName={animationPhase}
						loop={animationPhase === 'idle'}
						listener={{
							complete: () => {
								if (animationPhase === 'intro') {
									animationPhase = 'idle';
								}
							},
						}}
					/>
				</SpineProvider>

				<!-- Title -->
				<Container y={-SYMBOL_SIZE * 2.5}>
					<Sprite
						key="alpha_domination_title.png"
						anchor={0.5}
						width={SYMBOL_SIZE * 6}
						height={SYMBOL_SIZE * 1.5}
					/>
				</Container>

				<!-- Info Panel -->
				<Container y={SYMBOL_SIZE * 1.5}>
					<!-- Starting Multiplier -->
					<Container y={0}>
						<BitmapText
							anchor={0.5}
							text="STARTING MULTIPLIER"
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.3,
							}}
						/>
						<BitmapText
							anchor={0.5}
							y={SYMBOL_SIZE * 0.4}
							text={`x${introData.startingMultiplier}`}
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.8,
								fontWeight: 'bold',
							}}
						/>
					</Container>

					<!-- Multiplier Cap -->
					<Container y={SYMBOL_SIZE * 1.2}>
						<BitmapText
							anchor={0.5}
							text="MAX MULTIPLIER"
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.3,
							}}
						/>
						<BitmapText
							anchor={0.5}
							y={SYMBOL_SIZE * 0.4}
							text={`x${introData.multCap}`}
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.6,
								fontWeight: 'bold',
							}}
						/>
					</Container>

					<!-- Grid Info -->
					<Container y={SYMBOL_SIZE * 2.2}>
						<BitmapText
							anchor={0.5}
							text="8x8 GRID LOCKED"
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.35,
							}}
						/>
						<BitmapText
							anchor={0.5}
							y={SYMBOL_SIZE * 0.35}
							text={`${GRID_CONFIGS['8x8'].ways.toLocaleString()} WAYS`}
							style={{
								fontFamily: 'gold',
								fontSize: SYMBOL_SIZE * 0.25,
							}}
						/>
					</Container>

					<!-- Guaranteed Alpha Wolves -->
					{#if introData.guaranteedAlphaWolves > 0}
						<Container y={SYMBOL_SIZE * 3}>
							<BitmapText
								anchor={0.5}
								text={`+${introData.guaranteedAlphaWolves} ALPHA WOLVES GUARANTEED`}
								style={{
									fontFamily: 'gold',
									fontSize: SYMBOL_SIZE * 0.25,
								}}
							/>
						</Container>
					{/if}
				</Container>
			</Container>
		</MainContainer>

		<PressToContinue onpress={() => oncomplete()} />
	{/if}
</FadeContainer>
