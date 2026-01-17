<script lang="ts">
	import { onMount } from 'svelte';
	import { stateSound } from 'state-shared';

	// Enable sound system on mount
	onMount(() => {
		// Sound system initialization would happen here
		stateSound.enabled = true;
	});
</script>
