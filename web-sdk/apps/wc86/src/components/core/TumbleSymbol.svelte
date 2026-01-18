<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';
	import type { Container as PixiContainer } from 'pixi.js';
	import type { SymbolId } from '../../game/types';
	import { SYMBOL_INFO_MAP, SYMBOL_SIZE } from '../../game/constants';
	import { getSymbolInfo } from '../../game/utils';
	import SymbolSpine from './SymbolSpine.svelte';

	// Position with row/col for grid layout
	interface GridPosition {
		row: number;
		col: number;
	}

	interface Props {
		symbolId: SymbolId;
		position: GridPosition;
		cellWidth: number;
		cellHeight: number;
		isTumbling?: boolean;
		isWinning?: boolean;
		onTumbleComplete?: () => void;
	}

	let {
		symbolId,
		position,
		cellWidth,
		cellHeight,
		isTumbling = false,
		isWinning = false,
		onTumbleComplete
	}: Props = $props();

	let containerRef: PixiContainer | null = $state(null);
	let tumbleProgress = $state(0);

	// Get the current state for the symbol
	const currentState = $derived(isWinning ? 'win' : 'static');
	const symbolInfoForState = $derived(getSymbolInfo({
		rawSymbol: { name: symbolId },
		state: currentState
	}));
	const isSpineSymbol = $derived(symbolInfoForState?.type === 'spine');

	const x = $derived(position.col * cellWidth + cellWidth / 2);
	const y = $derived(position.row * cellHeight + cellHeight / 2);

	// Tumble animation effect
	$effect(() => {
		if (isTumbling && containerRef) {
			tumbleProgress = 0;
			const startY = y - cellHeight * 2;
			const targetY = y;
			const duration = 300;
			const startTime = performance.now();

			const animate = (currentTime: number) => {
				const elapsed = currentTime - startTime;
				const progress = Math.min(elapsed / duration, 1);

				// Easing function for bounce effect
				const easeOutBounce = (t: number) => {
					if (t < 1 / 2.75) {
						return 7.5625 * t * t;
					} else if (t < 2 / 2.75) {
						return 7.5625 * (t -= 1.5 / 2.75) * t + 0.75;
					} else if (t < 2.5 / 2.75) {
						return 7.5625 * (t -= 2.25 / 2.75) * t + 0.9375;
					} else {
						return 7.5625 * (t -= 2.625 / 2.75) * t + 0.984375;
					}
				};

				tumbleProgress = easeOutBounce(progress);

				if (containerRef) {
					containerRef.y = startY + (targetY - startY) * tumbleProgress;
				}

				if (progress < 1) {
					requestAnimationFrame(animate);
				} else {
					onTumbleComplete?.();
				}
			};

			requestAnimationFrame(animate);
		}
	});
</script>

<Container
	bind:instance={containerRef}
	{x}
	y={isTumbling ? y - cellHeight * 2 : y}
	alpha={1}
>
	{#if isSpineSymbol && symbolInfoForState}
		<SymbolSpine
			symbolInfo={symbolInfoForState}
			showWinFrame={isWinning}
			listener={{
				complete: onTumbleComplete,
			}}
		/>
	{:else if symbolInfoForState}
		<Sprite
			key={symbolInfoForState.assetKey}
			anchor={{ x: 0.5, y: 0.5 }}
			width={cellWidth * 0.9}
			height={cellHeight * 0.9}
		/>
	{/if}
</Container>
