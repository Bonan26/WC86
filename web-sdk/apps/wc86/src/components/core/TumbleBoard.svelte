<script lang="ts">
	import { Container } from 'pixi-svelte';
	import type { Container as PixiContainer } from 'pixi.js';
	import { getContext } from 'svelte';
	import type { SymbolId, GridSizeConfig, GameState } from '../../game/types';

	// Position with row/col for grid layout
	interface GridPosition {
		row: number;
		col: number;
	}
	import { GRID_CONFIGS } from '../../game/constants';
	import TumbleBoardBase from './TumbleBoardBase.svelte';
	import BoardMask from './BoardMask.svelte';
	import BoardFrame from './BoardFrame.svelte';

	interface Props {
		width?: number;
		height?: number;
	}

	let {
		width = 800,
		height = 600
	}: Props = $props();

	const gameState = getContext<{ current: GameState }>('gameState');

	let containerRef: PixiContainer | null = $state(null);
	let tumblingSymbols = $state<Set<string>>(new Set());
	let winningPositions = $state<Set<string>>(new Set());

	// Current grid size based on expansion level
	const currentGridSize = $derived.by((): GridSizeConfig => {
		const gridKey = gameState?.current?.currentGrid ?? '6x5';
		const config = GRID_CONFIGS[gridKey];
		return { rows: config.rows, cols: config.reels };
	});

	// Transform board data into symbol array
	const boardSymbols = $derived.by(() => {
		const board = gameState?.current?.board ?? [];
		const symbols: Array<{
			id: string;
			symbolId: SymbolId;
			position: GridPosition;
			isTumbling: boolean;
			isWinning: boolean;
		}> = [];

		board.forEach((row, rowIndex) => {
			row.forEach((symbolId, colIndex) => {
				if (symbolId !== null) {
					const id = `${rowIndex}-${colIndex}`;
					symbols.push({
						id,
						symbolId,
						position: { row: rowIndex, col: colIndex },
						isTumbling: tumblingSymbols.has(id),
						isWinning: winningPositions.has(id)
					});
				}
			});
		});

		return symbols;
	});

	// Handle tumble completion for cascading
	function handleSymbolTumbleComplete(symbolId: string) {
		tumblingSymbols.delete(symbolId);
		tumblingSymbols = new Set(tumblingSymbols);
	}

	// Start tumble animation for new symbols
	export function startTumble(positions: GridPosition[]) {
		const newTumbling = new Set<string>();
		positions.forEach(pos => {
			newTumbling.add(`${pos.row}-${pos.col}`);
		});
		tumblingSymbols = newTumbling;
	}

	// Set winning positions for highlight
	export function setWinningPositions(positions: GridPosition[]) {
		const newWinning = new Set<string>();
		positions.forEach(pos => {
			newWinning.add(`${pos.row}-${pos.col}`);
		});
		winningPositions = newWinning;
	}

	// Clear winning highlights
	export function clearWinningPositions() {
		winningPositions = new Set();
	}
</script>

<Container bind:instance={containerRef} x={0} y={0}>
	<!-- Board frame/border -->
	<BoardFrame {width} {height} />

	<!-- Masked board content -->
	<BoardMask {width} {height}>
		<TumbleBoardBase
			symbols={boardSymbols}
			gridSize={currentGridSize}
			{width}
			{height}
			onSymbolTumbleComplete={handleSymbolTumbleComplete}
		/>
	</BoardMask>
</Container>
