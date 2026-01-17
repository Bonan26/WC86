import { createLayout } from 'utils-layout';
import {
	BACKGROUND_RATIO,
	PORTRAIT_BACKGROUND_RATIO,
	DESKTOP_MAIN_SIZES,
	LANDSCAPE_MAIN_SIZES,
	PORTRAIT_MAIN_SIZES,
} from './constants';

export const { stateLayout, stateLayoutDerived } = createLayout({
	backgroundRatio: {
		normal: BACKGROUND_RATIO,
		portrait: PORTRAIT_BACKGROUND_RATIO,
	},
	mainSizesMap: {
		desktop: DESKTOP_MAIN_SIZES,
		tablet: { width: 1000, height: 1000 },
		landscape: LANDSCAPE_MAIN_SIZES,
		portrait: PORTRAIT_MAIN_SIZES,
	},
});
