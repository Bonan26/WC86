<script lang="ts" module>
	import type { TerritoryExpandData } from '../../game/types';

	export type EmitterEventTerritoryExpand =
		| { type: 'territoryUpdate'; count: number }
		| { type: 'territoryExpandAnimate'; data: TerritoryExpandData };
</script>

<script lang="ts">
	import { BitmapText, Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../../game/context';
	import { SYMBOL_SIZE, TERRITORY_THRESHOLDS, GRID_CONFIGS } from '../../game/constants';
	import type { GridSize } from '../../game/types';

	const context = getContext();

	// Territory progress tracking
	let territoryCount = $state(0);
	let visible = $state(true);

	// Calculate progress to next expansion
	const thresholds = [3, 6, 10];
	const nextThreshold = $derived(() => {
		for (const t of thresholds) {
			if (territoryCount < t) return t;
		}
		return 10; // Max
	});

	const progress = $derived(() => {
		const prevThreshold = thresholds.find((t, i) => {
			const prev = i === 0 ? 0 : thresholds[i - 1];
			return territoryCount >= prev && territoryCount < t;
		}) || 10;

		const prev = thresholds.indexOf(prevThreshold) === 0 ? 0 : thresholds[thresholds.indexOf(prevThreshold) - 1];
		return (territoryCount - prev) / (prevThreshold - prev);
	});

	const currentGrid = $derived(context.stateGame.currentGrid);
	const nextGrid = $derived(() => {
		const next = nextThreshold();
		return TERRITORY_THRESHOLDS[next as keyof typeof TERRITORY_THRESHOLDS] || currentGrid;
	});

	// Position on the right side of the board
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x +
			context.stateGameDerived.boardLayout().width * 0.5 + SYMBOL_SIZE * 0.5,
		y: context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.3,
	});

	context.eventEmitter.subscribeOnMount({
		territoryUpdate: ({ count }) => {
			territoryCount = count;
		},
		territoryExpandAnimate: ({ data }) => {
			territoryCount = data.territoryCount;
		},
	});

	// Sync with game state
	$effect(() => {
		territoryCount = context.stateGame.territoryCounter;
	});

	const PROGRESS_BAR_WIDTH = SYMBOL_SIZE * 0.3;
	const PROGRESS_BAR_HEIGHT = SYMBOL_SIZE * 2;
</script>

<MainContainer>
	<FadeContainer show={visible && territoryCount > 0} {...position}>
		<Container>
			<!-- Progress bar background -->
			<Rectangle
				width={PROGRESS_BAR_WIDTH}
				height={PROGRESS_BAR_HEIGHT}
				backgroundColor={0x1a1a2e}
				alpha={0.8}
			/>

			<!-- Progress bar fill -->
			<Rectangle
				y={PROGRESS_BAR_HEIGHT * (1 - progress())}
				width={PROGRESS_BAR_WIDTH}
				height={PROGRESS_BAR_HEIGHT * progress()}
				backgroundColor={0x7b2cbf}
			/>

			<!-- Progress bar border -->
			<Rectangle
				width={PROGRESS_BAR_WIDTH}
				height={PROGRESS_BAR_HEIGHT}
				backgroundColor={0x000000}
				alpha={0}
			/>

			<!-- Territory icon -->
			<Sprite
				key="territory_icon.png"
				anchor={0.5}
				x={PROGRESS_BAR_WIDTH / 2}
				y={-SYMBOL_SIZE * 0.3}
				width={SYMBOL_SIZE * 0.4}
				height={SYMBOL_SIZE * 0.4}
			/>

			<!-- Count display -->
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={PROGRESS_BAR_WIDTH / 2}
				y={PROGRESS_BAR_HEIGHT + SYMBOL_SIZE * 0.1}
				text={`${territoryCount}/${nextThreshold()}`}
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.2,
				}}
			/>

			<!-- Next grid size indicator -->
			<BitmapText
				anchor={{ x: 0.5, y: 0 }}
				x={PROGRESS_BAR_WIDTH / 2}
				y={PROGRESS_BAR_HEIGHT + SYMBOL_SIZE * 0.35}
				text={nextGrid()}
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.15,
				}}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
