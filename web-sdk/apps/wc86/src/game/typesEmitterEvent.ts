import type { EmitterEventBoard } from '../components/core/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/core/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/core/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinCounter } from '../components/core/FreeSpinCounter.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/core/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/core/Win.svelte';
import type { EmitterEventSound } from '../components/core/Sound.svelte';
import type { EmitterEventTransition } from '../components/core/Transition.svelte';
import type { EmitterEventHuntMultiplier } from '../components/custom/HuntMultiplier.svelte';
import type { EmitterEventPackSplit } from '../components/custom/PackSplitAnimation.svelte';
import type { EmitterEventHowlChain } from '../components/custom/HowlChainEffect.svelte';
import type { EmitterEventGridExpansion } from '../components/custom/GridExpansion.svelte';
import type { EmitterEventAlphaDomination } from '../components/custom/AlphaDominationIntro.svelte';
import type { EmitterEventTerritoryExpand } from '../components/custom/TerritoryExpand.svelte';
import type { EmitterEventVolatilitySelector } from '../components/custom/VolatilitySelector.svelte';

export type EmitterEventGame =
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinCounter
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventHuntMultiplier
	| EmitterEventPackSplit
	| EmitterEventHowlChain
	| EmitterEventGridExpansion
	| EmitterEventAlphaDomination
	| EmitterEventTerritoryExpand
	| EmitterEventVolatilitySelector;
