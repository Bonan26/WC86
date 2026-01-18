<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { onMount } from 'svelte';

	import { getSymbolInfo } from '../../game/utils';
	import { SYMBOL_SIZE } from '../../game/constants';

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
	};

	const props: Props = $props();

	onMount(() => {
		props.oncomplete?.();
	});

	$effect(() => {
		props.symbolInfo;
		props.oncomplete?.();
	});
</script>

{#if props.symbolInfo}
	<Sprite
		x={props.x}
		y={props.y}
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		width={SYMBOL_SIZE * (props.symbolInfo.sizeRatios?.width || 1)}
		height={SYMBOL_SIZE * (props.symbolInfo.sizeRatios?.height || 1)}
	/>
{/if}
