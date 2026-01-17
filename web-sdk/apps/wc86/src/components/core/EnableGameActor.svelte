<script lang="ts">
	import { onMount } from 'svelte';
	import { getContext } from '../../game/context';

	const context = getContext();

	// Enable game actor/state machine on mount
	onMount(() => {
		// Game actor initialization would happen here
		console.log('Game actor enabled');
	});
</script>
