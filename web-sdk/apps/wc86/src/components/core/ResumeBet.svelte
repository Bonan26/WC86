<script lang="ts">
	import { onMount } from 'svelte';
	import { getContext } from '../../game/context';

	const context = getContext();

	// Handle bet resumption after page reload
	onMount(() => {
		// Resume bet logic would happen here
		console.log('Resume bet check');
	});
</script>
