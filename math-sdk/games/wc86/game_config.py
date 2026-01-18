"""
WC86 - Wolf Club 86
Game Configuration - High Volatility 6x5→8x8 Ways Slot
Theme: Nightclub retro 80s with wolves
"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class VolatilityMode:
    """Volatility mode constants."""
    LONE_WOLF = "LONE_WOLF"  # 96.8% RTP, 10,000x max, 50 mult cap
    PACK = "PACK"            # 96.5% RTP, 25,000x max, 200 mult cap
    ALPHA = "ALPHA"          # 96.2% RTP, 50,000x max, 500 mult cap


class GridSize:
    """Grid size constants."""
    BASE = "6x5"      # 7,776 ways
    EXPAND_1 = "7x6"  # 46,656 ways
    EXPAND_2 = "8x7"  # 117,649 ways
    MAX = "8x8"       # 262,144 ways


class GameConfig(Config):
    """WC86 game configuration."""

    _instance = None

    def __new__(cls, volatility_mode=VolatilityMode.PACK):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, volatility_mode=VolatilityMode.PACK):
        super().__init__()
        self.volatility_mode = volatility_mode

        # Game identification
        self.game_id = "wc86"
        self.provider_number = 86
        self.working_name = "Wolf Club 86"
        self.win_type = "ways"

        # Volatility-dependent settings
        self._setup_volatility_settings()

        self.construct_paths()

        # Grid Configuration - Dynamic 6x5 → 8x8
        self.base_num_reels = 6
        self.base_num_rows = 5
        self.num_reels = self.base_num_reels
        self.num_rows = [self.base_num_rows] * self.num_reels

        # Grid expansion thresholds (territory symbols collected)
        self.grid_expansion_thresholds = {
            3: GridSize.EXPAND_1,   # 7x6
            6: GridSize.EXPAND_2,   # 8x7
            10: GridSize.MAX,       # 8x8
        }

        # Ways count per grid size
        self.ways_count = {
            GridSize.BASE: 7776,
            GridSize.EXPAND_1: 46656,
            GridSize.EXPAND_2: 117649,
            GridSize.MAX: 262144,
        }

        # Paytable - (kind, symbol): payout multiplier
        self.paytable = self._build_paytable()

        # Symbol configuration (no underscores - SDK strips them from CSV)
        self.include_padding = True
        self.special_symbols = {
            "wild": ["ALPHAWOLF", "HOWLINGWILD"],
            "scatter": ["MOONSCATTER"],
            "multiplier": ["HOWLINGWILD"],
            "territory": ["TERRITORY"],
        }

        # Howling Wild multiplier values
        self.howling_wild_multipliers = {
            2: 40,
            3: 25,
            5: 20,
            10: 12,
            15: 3,
        }

        # Pack Split configuration (Alpha Wolf duplication)
        self.pack_split_chances = {
            2: 50,
            3: 35,
            4: 15,
        }

        # Free Spin triggers based on scatter count
        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 12, 5: 15, 6: 20},
            self.freegame_type: {2: 3, 3: 5, 4: 8, 5: 10, 6: 15},
        }

        # Anticipation triggers
        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 1,
        }

        # Load reels
        self._load_reels()

        # Setup bet modes
        self.bet_modes = self._build_bet_modes()

    def _setup_volatility_settings(self):
        """Configure settings based on volatility mode."""
        settings = {
            VolatilityMode.LONE_WOLF: {
                "rtp": 0.968,
                "wincap": 10000,
                "fs_mult_cap": 50,
                "base_mult_cap": 20,
            },
            VolatilityMode.PACK: {
                "rtp": 0.965,
                "wincap": 25000,
                "fs_mult_cap": 200,
                "base_mult_cap": 30,
            },
            VolatilityMode.ALPHA: {
                "rtp": 0.962,
                "wincap": 50000,
                "fs_mult_cap": 500,
                "base_mult_cap": 50,
            },
        }

        mode_settings = settings[self.volatility_mode]
        self.rtp = mode_settings["rtp"]
        self.wincap = mode_settings["wincap"]
        self.fs_mult_cap = mode_settings["fs_mult_cap"]
        self.base_mult_cap = mode_settings["base_mult_cap"]

    def _build_paytable(self):
        """
        Build paytable calibrated for 96.5% RTP.
        Values optimized for ways-pay mechanics.
        """
        # Calibré pour 96.5% RTP (facteur 0.995 appliqué)
        return {
            # BOSSWOLF - highest pay
            (6, "BOSSWOLF"): 2.335,
            (5, "BOSSWOLF"): 1.168,
            (4, "BOSSWOLF"): 0.471,
            (3, "BOSSWOLF"): 0.228,

            # HUSTLER
            (6, "HUSTLER"): 1.570,
            (5, "HUSTLER"): 0.778,
            (4, "HUSTLER"): 0.309,
            (3, "HUSTLER"): 0.161,

            # TECHBRO
            (6, "TECHBRO"): 1.100,
            (5, "TECHBRO"): 0.550,
            (4, "TECHBRO"): 0.228,
            (3, "TECHBRO"): 0.108,

            # DIAMONDHANDS
            (6, "DIAMONDHANDS"): 0.778,
            (5, "DIAMONDHANDS"): 0.389,
            (4, "DIAMONDHANDS"): 0.161,
            (3, "DIAMONDHANDS"): 0.080,

            # COCKTAIL
            (6, "COCKTAIL"): 0.228,
            (5, "COCKTAIL"): 0.121,
            (4, "COCKTAIL"): 0.047,
            (3, "COCKTAIL"): 0.023,

            # VIPCARD
            (6, "VIPCARD"): 0.174,
            (5, "VIPCARD"): 0.090,
            (4, "VIPCARD"): 0.039,
            (3, "VIPCARD"): 0.017,

            # DISCOBALL
            (6, "DISCOBALL"): 0.157,
            (5, "DISCOBALL"): 0.077,
            (4, "DISCOBALL"): 0.031,
            (3, "DISCOBALL"): 0.016,

            # DICE
            (6, "DICE"): 0.110,
            (5, "DICE"): 0.055,
            (4, "DICE"): 0.023,
            (3, "DICE"): 0.011,
        }

    def _load_reels(self):
        """Load all reel configurations from CSV files."""
        reel_files = {
            f"BR_{self.volatility_mode}": f"BR_{self.volatility_mode}.csv",
            f"FR_{self.volatility_mode}": f"FR_{self.volatility_mode}.csv",
            f"FR_WINCAP_{self.volatility_mode}": f"FR_WINCAP_{self.volatility_mode}.csv",
            "AD_REELS": "AD_REELS.csv",
            "AD_WINCAP": "AD_WINCAP.csv",
        }

        self.reels = {}
        for reel_name, filename in reel_files.items():
            reel_path = os.path.join(self.reels_path, filename)
            if os.path.exists(reel_path):
                self.reels[reel_name] = self.read_reels_csv(reel_path)
            else:
                self.reels[reel_name] = None

    def _build_bet_modes(self):
        """Build the 4 bet modes with their distributions."""
        mode_maxwins = {
            "base": self.wincap,
            "pack_hunt": self.wincap,
            "pack_hunt_plus": self.wincap,
            "alpha_domination": self.wincap,
        }

        return [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.0005,
                        win_criteria=mode_maxwins["base"],
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {f"BR_{self.volatility_mode}": 1},
                                self.freegame_type: {
                                    f"FR_{self.volatility_mode}": 1,
                                    f"FR_WINCAP_{self.volatility_mode}": 10,
                                },
                            },
                            "force_wincap": True,
                            "force_freegame": True,
                            "scatter_triggers": {3: 100, 4: 30, 5: 10, 6: 2},
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": self.fs_mult_cap,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.08,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {f"BR_{self.volatility_mode}": 1},
                                self.freegame_type: {f"FR_{self.volatility_mode}": 1},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {3: 100, 4: 20, 5: 5, 6: 1},
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": self.fs_mult_cap,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.35,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {f"BR_{self.volatility_mode}": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": {1: 1},
                            "hunt_mult_cap": self.base_mult_cap,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.57,
                        conditions={
                            "reel_weights": {self.basegame_type: {f"BR_{self.volatility_mode}": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": self.base_mult_cap,
                        },
                    ),
                ],
            ),

            BetMode(
                name="pack_hunt",
                cost=75.0,
                rtp=self.rtp,
                max_win=mode_maxwins["pack_hunt"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {f"BR_{self.volatility_mode}": 1},
                                self.freegame_type: {
                                    f"FR_{self.volatility_mode}": 1,
                                    f"FR_WINCAP_{self.volatility_mode}": 5,
                                },
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {3: 100, 4: 20, 5: 5, 6: 1},
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": self.fs_mult_cap,
                            "starting_multiplier": 1,
                        },
                    ),
                ],
            ),

            BetMode(
                name="pack_hunt_plus",
                cost=150.0,
                rtp=self.rtp,
                max_win=mode_maxwins["pack_hunt_plus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {f"BR_{self.volatility_mode}": 1},
                                self.freegame_type: {
                                    f"FR_{self.volatility_mode}": 1,
                                    f"FR_WINCAP_{self.volatility_mode}": 8,
                                },
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {3: 100, 4: 25, 5: 8, 6: 2},
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": self.fs_mult_cap,
                            "starting_multiplier": 3,
                        },
                    ),
                ],
            ),

            BetMode(
                name="alpha_domination",
                cost=500.0,
                rtp=self.rtp,
                max_win=mode_maxwins["alpha_domination"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="alpha_domination",
                        quota=1.0,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"AD_REELS": 1},
                                self.freegame_type: {"AD_REELS": 1, "AD_WINCAP": 10},
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                            "force_alpha_domination": True,
                            "mult_values": self.howling_wild_multipliers,
                            "hunt_mult_cap": 500,
                            "starting_multiplier": 5,
                            "guaranteed_alpha_wolves": 2,
                            "grid_size": GridSize.MAX,
                        },
                    ),
                ],
            ),
        ]

    def get_mult_cap(self, gametype):
        """Get multiplier cap based on game type."""
        if gametype == self.basegame_type:
            return self.base_mult_cap
        return self.fs_mult_cap

    def get_grid_config(self, grid_size):
        """Get grid dimensions for a given grid size."""
        configs = {
            GridSize.BASE: {"reels": 6, "rows": 5},
            GridSize.EXPAND_1: {"reels": 7, "rows": 6},
            GridSize.EXPAND_2: {"reels": 8, "rows": 7},
            GridSize.MAX: {"reels": 8, "rows": 8},
        }
        return configs.get(grid_size, configs[GridSize.BASE])

    def check_grid_expansion(self, territory_count, current_grid):
        """Check if grid should expand based on territory collected."""
        for threshold, new_grid in sorted(self.grid_expansion_thresholds.items()):
            if territory_count >= threshold and current_grid != new_grid:
                grid_order = [GridSize.BASE, GridSize.EXPAND_1, GridSize.EXPAND_2, GridSize.MAX]
                current_idx = grid_order.index(current_grid) if current_grid in grid_order else 0
                new_idx = grid_order.index(new_grid)
                if new_idx > current_idx:
                    return new_grid
        return None

    def get_howl_chain_multiplier(self, wild_positions, board):
        """Calculate Howl Chain multiplier."""
        if len(wild_positions) < 2:
            return 1, "none"

        multipliers = []
        for pos in wild_positions:
            symbol = board[pos["reel"]][pos["row"]]
            if hasattr(symbol, "multiplier") and symbol.multiplier:
                multipliers.append(symbol.multiplier)
            else:
                multipliers.append(1)

        if len(wild_positions) == 2:
            return sum(multipliers), "additive"
        else:
            result = 1
            for m in multipliers:
                result *= m
            return result, "multiplicative"
