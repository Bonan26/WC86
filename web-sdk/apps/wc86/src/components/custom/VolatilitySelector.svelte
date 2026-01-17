<script lang="ts" module>
	export type EmitterEventVolatilitySelector =
		| { type: 'volatilitySelectorShow' }
		| { type: 'volatilitySelectorHide' }
		| { type: 'volatilitySelected'; mode: 'LONE_WOLF' | 'PACK' | 'ALPHA' };
</script>

<script lang="ts">
	import { BitmapText, Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer, CanvasSizeRectangle } from 'components-layout';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE } from '../../game/constants';
	import type { VolatilityMode } from '../../game/types';

	const context = getContext();

	let visible = $state(false);
	let selectedMode = $state<VolatilityMode>('PACK');

	const volatilityModes = [
		{
			id: 'LONE_WOLF' as VolatilityMode,
			name: 'LONE WOLF',
			icon: '🐺',
			rtp: '96.8%',
			maxWin: '10,000x',
			hitFreq: '~35%',
			description: 'Lower risk, more frequent wins',
			color: 0x4a9eff,
		},
		{
			id: 'PACK' as VolatilityMode,
			name: 'PACK',
			icon: '🐺🐺',
			rtp: '96.5%',
			maxWin: '25,000x',
			hitFreq: '~25%',
			description: 'Balanced risk and reward',
			color: 0x9b59b6,
		},
		{
			id: 'ALPHA' as VolatilityMode,
			name: 'ALPHA',
			icon: '🐺🐺🐺',
			rtp: '96.2%',
			maxWin: '50,000x',
			hitFreq: '~15%',
			description: 'High risk, massive potential',
			color: 0xff4757,
		},
	];

	const selectMode = (mode: VolatilityMode) => {
		selectedMode = mode;
		context.stateGame.volatilityMode = mode;
		context.eventEmitter.broadcast({ type: 'volatilitySelected', mode });
	};

	context.eventEmitter.subscribeOnMount({
		volatilitySelectorShow: () => {
			visible = true;
		},
		volatilitySelectorHide: () => {
			visible = false;
		},
	});

	const CARD_WIDTH = SYMBOL_SIZE * 2.5;
	const CARD_HEIGHT = SYMBOL_SIZE * 3.5;
	const CARD_GAP = SYMBOL_SIZE * 0.5;
</script>

<FadeContainer show={visible}>
	<CanvasSizeRectangle backgroundColor={0x0a0a14} backgroundAlpha={0.95} />

	<MainContainer>
		<Container
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
		>
			<!-- Title -->
			<BitmapText
				anchor={0.5}
				y={-SYMBOL_SIZE * 3}
				text="SELECT VOLATILITY"
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.6,
					fontWeight: 'bold',
				}}
			/>

			<!-- Mode Cards -->
			{#each volatilityModes as mode, index}
				{@const xOffset = (index - 1) * (CARD_WIDTH + CARD_GAP)}
				{@const isSelected = selectedMode === mode.id}

				<Container
					x={xOffset}
					y={0}
					interactive={true}
					cursor="pointer"
					onclick={() => selectMode(mode.id)}
				>
					<!-- Card Background -->
					<Rectangle
						x={-CARD_WIDTH / 2}
						y={-CARD_HEIGHT / 2}
						width={CARD_WIDTH}
						height={CARD_HEIGHT}
						backgroundColor={isSelected ? mode.color : 0x1a1a2e}
						alpha={isSelected ? 1 : 0.8}
					/>

					<!-- Card Border -->
					<Rectangle
						x={-CARD_WIDTH / 2}
						y={-CARD_HEIGHT / 2}
						width={CARD_WIDTH}
						height={CARD_HEIGHT}
						backgroundColor={mode.color}
						alpha={isSelected ? 0 : 0.3}
					/>

					<!-- Mode Name -->
					<BitmapText
						anchor={0.5}
						y={-CARD_HEIGHT * 0.35}
						text={mode.name}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.3,
							fontWeight: 'bold',
						}}
					/>

					<!-- Wolf Icon -->
					<BitmapText
						anchor={0.5}
						y={-CARD_HEIGHT * 0.15}
						text={mode.icon}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.5,
						}}
					/>

					<!-- RTP -->
					<BitmapText
						anchor={0.5}
						y={CARD_HEIGHT * 0.05}
						text={`RTP: ${mode.rtp}`}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.2,
						}}
					/>

					<!-- Max Win -->
					<BitmapText
						anchor={0.5}
						y={CARD_HEIGHT * 0.15}
						text={`MAX: ${mode.maxWin}`}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.22,
							fontWeight: 'bold',
						}}
					/>

					<!-- Hit Frequency -->
					<BitmapText
						anchor={0.5}
						y={CARD_HEIGHT * 0.25}
						text={`HIT: ${mode.hitFreq}`}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.18,
						}}
					/>

					<!-- Description -->
					<BitmapText
						anchor={0.5}
						y={CARD_HEIGHT * 0.38}
						text={mode.description}
						style={{
							fontFamily: 'gold',
							fontSize: SYMBOL_SIZE * 0.12,
							wordWrap: true,
							wordWrapWidth: CARD_WIDTH * 0.9,
							align: 'center',
						}}
					/>
				</Container>
			{/each}

			<!-- Confirm Button -->
			<Container
				y={SYMBOL_SIZE * 2.5}
				interactive={true}
				cursor="pointer"
				onclick={() => (visible = false)}
			>
				<Rectangle
					x={-SYMBOL_SIZE * 1.5}
					y={-SYMBOL_SIZE * 0.3}
					width={SYMBOL_SIZE * 3}
					height={SYMBOL_SIZE * 0.6}
					backgroundColor={0x27ae60}
				/>
				<BitmapText
					anchor={0.5}
					text="CONFIRM"
					style={{
						fontFamily: 'gold',
						fontSize: SYMBOL_SIZE * 0.3,
						fontWeight: 'bold',
					}}
				/>
			</Container>
		</Container>
	</MainContainer>
</FadeContainer>
