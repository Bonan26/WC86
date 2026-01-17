<script lang="ts">
	import type { Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderStakeEngine, LoadI18n } from 'components-shared';

	import { setContext } from '../game/context';
	import { stateApp } from '../game/stateApp';
	import { messages } from '../i18n/messages';

	interface Props {
		children: Snippet;
	}

	const props: Props = $props();

	// Set up all context providers
	setContext();

	// Type assertions for SDK components with strict type definitions
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const messagesMap = messages as any;
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const LoaderStakeEngineAny = LoaderStakeEngine as any;
</script>

<GlobalStyle>
	<Authenticate>
		<LoadI18n {messagesMap}>
			{#snippet children()}
				<LoaderStakeEngineAny
					onloaded={() => {
						stateApp.loaded = true;
					}}
				>
					{#snippet children()}
						{@render props.children()}
					{/snippet}
				</LoaderStakeEngineAny>
			{/snippet}
		</LoadI18n>
	</Authenticate>
</GlobalStyle>
