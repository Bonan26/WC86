<script lang="ts">
	import { Container } from 'pixi-svelte';
	import type { Container as PixiContainer } from 'pixi.js';
	import type { SymbolId, GridSizeConfig } from '../../game/types';
	import TumbleSymbol from './TumbleSymbol.svelte';

	// Position with row/col for grid layout
	interface GridPosition {
		row: number;
		col: number;
	}

	interface BoardSymbol {
		id: string;
		symbolId: SymbolId;
		position: GridPosition;
		isTumbling: boolean;
		isWinning: boolean;
	}

	interface Props {
		symbols: BoardSymbol[];
		gridSize: GridSizeConfig;
		width: number;
		height: number;
		onSymbolTumbleComplete?: (symbolId: string) => void;
	}

	let {
		symbols,
		gridSize,
		width,
		height,
		onSymbolTumbleComplete
	}: Props = $props();

	let containerRef: PixiContainer | null = $state(null);

	const cellWidth = $derived(width / gridSize.cols);
	const cellHeight = $derived(height / gridSize.rows);

	function handleTumbleComplete(symbolUniqueId: string) {
		onSymbolTumbleComplete?.(symbolUniqueId);
	}
</script>

<Container bind:instance={containerRef} x={0} y={0}>
	{#each symbols as symbol (symbol.id)}
		<TumbleSymbol
			symbolId={symbol.symbolId}
			position={symbol.position}
			{cellWidth}
			{cellHeight}
			isTumbling={symbol.isTumbling}
			isWinning={symbol.isWinning}
			onTumbleComplete={() => handleTumbleComplete(symbol.id)}
		/>
	{/each}
</Container>
