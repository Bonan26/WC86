<script lang="ts" module>
	export type EmitterEventHuntMultiplier =
		| { type: 'huntMultiplierShow' }
		| { type: 'huntMultiplierHide' }
		| { type: 'huntMultiplierUpdate'; huntMultiplier: number; cascadeCount: number; multCap: number };
</script>

<script lang="ts">
	import { SpineProvider, SpineTrack, BitmapText, Container } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE } from '../../game/constants';

	const context = getContext();

	let visible = $state(false);
	let multiplier = $state(1);
	let cascadeCount = $state(0);
	let multCap = $state(50);
	let animation = $state<'idle' | 'increase' | 'maxed'>('idle');

	// Position multiplier display above the board
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x,
		y: context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.5 - SYMBOL_SIZE * 0.8,
	});

	context.eventEmitter.subscribeOnMount({
		huntMultiplierShow: () => {
			visible = true;
		},
		huntMultiplierHide: () => {
			visible = false;
			multiplier = 1;
			cascadeCount = 0;
		},
		huntMultiplierUpdate: (data) => {
			const prevMultiplier = multiplier;
			multiplier = data.huntMultiplier;
			cascadeCount = data.cascadeCount;
			multCap = data.multCap;

			if (multiplier >= multCap) {
				animation = 'maxed';
			} else if (multiplier > prevMultiplier) {
				animation = 'increase';
			}
		},
	});

	const handleAnimationComplete = () => {
		if (animation === 'increase') {
			animation = 'idle';
		}
	};
</script>

<MainContainer>
	<FadeContainer show={visible} {...position}>
		<Container>
			<!-- Hunt Multiplier Spine Animation -->
			<SpineProvider key="huntMultiplier" width={SYMBOL_SIZE * 1.5}>
				<SpineTrack
					trackIndex={0}
					animationName={animation}
					loop={animation === 'idle' || animation === 'maxed'}
					listener={{
						complete: handleAnimationComplete,
					}}
				/>
			</SpineProvider>

			<!-- Multiplier Value Text -->
			<BitmapText
				anchor={0.5}
				y={SYMBOL_SIZE * 0.1}
				text={`x${multiplier}`}
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.5,
					fontWeight: 'bold',
				}}
			/>

			<!-- Cascade Count Indicator -->
			{#if cascadeCount > 0}
				<BitmapText
					anchor={0.5}
					y={SYMBOL_SIZE * 0.5}
					text={`CASCADE ${cascadeCount}`}
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.2,
					}}
				/>
			{/if}
		</Container>
	</FadeContainer>
</MainContainer>
