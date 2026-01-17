import type { WinLevelMap } from 'utils-shared/winLevel';

export type WinLevelAlias = 'big' | 'super' | 'mega' | 'epic' | 'max' | 'none';

export type WinLevelData = {
	alias: WinLevelAlias;
	type: 'small' | 'big';
	presentDuration: number;
	animation?: {
		intro: string;
		idle: string;
		outro: string;
	};
};

// Win level thresholds (in multiples of bet)
export const winLevelMap: WinLevelMap<WinLevelAlias> = {
	none: { threshold: 0 },
	big: { threshold: 20 },
	super: { threshold: 50 },
	mega: { threshold: 100 },
	epic: { threshold: 500 },
	max: { threshold: 1000 },
};

// Win level data for animations and display
export const winLevelDataMap: Record<WinLevelAlias, WinLevelData> = {
	none: {
		alias: 'none',
		type: 'small',
		presentDuration: 1000,
	},
	big: {
		alias: 'big',
		type: 'big',
		presentDuration: 3000,
		animation: {
			intro: 'big_win_intro',
			idle: 'big_win_idle',
			outro: 'big_win_exit',
		},
	},
	super: {
		alias: 'super',
		type: 'big',
		presentDuration: 4000,
		animation: {
			intro: 'super_win_intro',
			idle: 'super_win_idle',
			outro: 'super_win_exit',
		},
	},
	mega: {
		alias: 'mega',
		type: 'big',
		presentDuration: 5000,
		animation: {
			intro: 'mega_win_intro',
			idle: 'mega_win_idle',
			outro: 'mega_win_exit',
		},
	},
	epic: {
		alias: 'epic',
		type: 'big',
		presentDuration: 6000,
		animation: {
			intro: 'epic_win_intro',
			idle: 'epic_win_idle',
			outro: 'epic_win_exit',
		},
	},
	max: {
		alias: 'max',
		type: 'big',
		presentDuration: 8000,
		animation: {
			intro: 'max_win_intro',
			idle: 'max_win_idle',
			outro: 'max_win_exit',
		},
	},
};
