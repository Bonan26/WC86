import { createLayout } from 'utils-layout';
import {
	BOARD_SIZES,
	DESKTOP_MAIN_SIZES,
	LANDSCAPE_MAIN_SIZES,
	PORTRAIT_MAIN_SIZES,
	BACKGROUND_RATIO,
	PORTRAIT_BACKGROUND_RATIO,
} from './constants';

export const { stateLayout, stateLayoutDerived } = createLayout({
	desktopMainSizes: DESKTOP_MAIN_SIZES,
	landscapeMainSizes: LANDSCAPE_MAIN_SIZES,
	portraitMainSizes: PORTRAIT_MAIN_SIZES,
	boardSizes: BOARD_SIZES,
	backgroundRatio: BACKGROUND_RATIO,
	portraitBackgroundRatio: PORTRAIT_BACKGROUND_RATIO,
});
