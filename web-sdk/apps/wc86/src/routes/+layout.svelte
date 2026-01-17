<script lang="ts">
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderStakeEngine, LoadI18n } from 'components-shared';
	import { stateConfig } from 'state-shared';

	import { setContext } from '../game/context';
	import { stateApp } from '../game/stateApp';
	import assets from '../game/assets';

	// Set up all context providers
	setContext();

	// Configure game
	stateConfig.gameName = 'wc86';
	stateConfig.gameDisplayName = 'Wolf Club 86';
</script>

<GlobalStyle />

<Authenticate>
	<LoadI18n>
		<LoaderStakeEngine
			{assets}
			onloaded={() => {
				stateApp.loaded = true;
			}}
		>
			<slot />
		</LoaderStakeEngine>
	</LoadI18n>
</Authenticate>
