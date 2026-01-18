"""
WC86 - Wolf Club 86
Game Override - Special symbol functions and state reset
"""

from games.wc86.game_executables import GameExecutables
from games.wc86.game_config import GridSize
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    Override base state functions for WC86 specific behavior.
    Handles special symbol assignments and book reset.
    """

    def reset_book(self):
        """
        Reset all game state for a new spin/book.
        Called at the start of each new simulation.
        """
        # Reset global values from parent
        super().reset_book()

        # WC86 specific state reset
        self.hunt_multiplier = 1
        self.cascade_count = 0
        self.territory_collected = 0
        self.current_grid = GridSize.BASE
        self.max_hunt_multiplier = 1

        # Reset grid to base dimensions
        self.config.num_reels = self.config.base_num_reels
        self.config.num_rows = [self.config.base_num_rows] * self.config.num_reels

        # Only check conditions if betmode is set (not during __init__)
        if hasattr(self, 'betmode') and self.betmode:
            conditions = self.get_current_distribution_conditions()

            # Check for starting multiplier from bet mode (pack_hunt_plus starts at x3)
            if "starting_multiplier" in conditions:
                self.hunt_multiplier = conditions["starting_multiplier"]

            # Check for forced grid size (alpha_domination uses 8x8)
            if "grid_size" in conditions:
                self.current_grid = conditions["grid_size"]
                grid_config = self.config.get_grid_config(self.current_grid)
                self.config.num_reels = grid_config["reels"]
                self.config.num_rows = [grid_config["rows"]] * grid_config["reels"]

    def reset_fs_spin(self):
        """Reset state for a new free spin within a free spin session."""
        super().reset_fs_spin()

        # Preserve hunt multiplier between spins in free games
        # (it persists and continues to increase)

        # Track max multiplier reached
        if self.hunt_multiplier > self.max_hunt_multiplier:
            self.max_hunt_multiplier = self.hunt_multiplier

    def assign_special_sym_function(self):
        """
        Define special functions to call when specific symbols are drawn.
        Maps symbol names to their processing functions.
        """
        self.special_symbol_functions = {
            "HOWLINGWILD": [self.assign_howling_wild_multiplier],
            "ALPHAWOLF": [self.assign_alpha_wolf_properties],
            "MOONSCATTER": [self.assign_scatter_properties],
            "TERRITORY": [self.assign_territory_properties],
        }

    def assign_howling_wild_multiplier(self, symbol):
        """
        Assign a random multiplier to HOWLING_WILD symbol.
        Multiplier values: x2, x3, x5, x10, x15 with weighted probabilities.
        """
        # Get multiplier values from conditions if betmode is set, else use default
        if hasattr(self, 'betmode') and self.betmode:
            conditions = self.get_current_distribution_conditions()
            mult_values = conditions.get("mult_values", self.config.howling_wild_multipliers)
        else:
            mult_values = self.config.howling_wild_multipliers

        multiplier_value = get_random_outcome(mult_values)

        symbol.assign_attribute({
            "multiplier": multiplier_value,
            "wild": True,
        })

    def assign_alpha_wolf_properties(self, symbol):
        """
        Assign wild property to ALPHA_WOLF symbol.
        Pack Split is processed separately in game_executables.
        """
        symbol.assign_attribute({"wild": True})

    def assign_scatter_properties(self, symbol):
        """Assign scatter property to MOON_SCATTER symbol."""
        symbol.assign_attribute({"scatter": True})

    def assign_territory_properties(self, symbol):
        """
        Territory property is handled via special_flags in the SDK.
        No additional attributes needed - just check special_flags for "territory".
        """
        pass  # SDK handles via special_flags from config.special_symbols

    def check_game_repeat(self):
        """
        Verify final simulation outcomes satisfied all distribution/criteria conditions.
        Used for forced outcomes (wincap, freegame triggers, etc.)
        """
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True

    def get_current_reel_name(self):
        """
        Get the current reel strip name based on game type and conditions.
        """
        conditions = self.get_current_distribution_conditions()
        reel_weights = conditions.get("reel_weights", {})

        if self.gametype in reel_weights:
            # Select reel based on weights
            reels = reel_weights[self.gametype]
            return get_random_outcome(reels)

        # Default fallback
        return f"BR_{self.config.volatility_mode}"

    def draw_board(self, emit_event=True):
        """
        Override draw_board to use WC86 specific reveal event.
        """
        super().draw_board(emit_event=False)

        if emit_event:
            from game_events import reveal_wc86_event
            reveal_wc86_event(self)

    def update_freespin_amount(self, scatter_key="scatter"):
        """
        Override to use WC86 specific free spin trigger event.
        """
        scatter_count = self.count_special_symbols(scatter_key)
        self.tot_fs = self.config.freespin_triggers[self.gametype][scatter_count]

        # Get scatter positions
        scatter_positions = []
        for reel_idx, reel_data in enumerate(self.special_syms_on_board.get(scatter_key, [])):
            if reel_data:
                scatter_positions.append({"reel": reel_idx, "row": reel_data.get("row", 0)})

        is_retrigger = self.gametype == self.config.freegame_type

        from game_events import freespin_trigger_wc86_event
        freespin_trigger_wc86_event(
            self,
            scatter_positions=scatter_positions,
            total_spins=self.tot_fs,
            is_retrigger=is_retrigger,
        )

    def end_freespin(self):
        """Override to use WC86 specific free spin end event."""
        from game_events import freespin_end_wc86_event
        freespin_end_wc86_event(self)

    def enter_alpha_domination(self):
        """
        Initialize state for Alpha Domination super bonus.
        Called when alpha_domination bet mode is selected.
        """
        conditions = self.get_current_distribution_conditions()

        # Set starting multiplier (min 5)
        self.hunt_multiplier = conditions.get("starting_multiplier", 5)

        # Set grid to 8x8
        self.current_grid = GridSize.MAX
        grid_config = self.config.get_grid_config(GridSize.MAX)
        self.config.num_reels = grid_config["reels"]
        self.config.num_rows = [grid_config["rows"]] * grid_config["reels"]

        # Emit alpha domination start event
        from game_events import alpha_domination_start_event
        alpha_domination_start_event(
            self,
            starting_multiplier=self.hunt_multiplier,
            mult_cap=conditions.get("hunt_mult_cap", 500),
            guaranteed_alpha_wolves=conditions.get("guaranteed_alpha_wolves", 2),
        )

    def end_alpha_domination(self):
        """End Alpha Domination and emit end event."""
        from game_events import alpha_domination_end_event
        alpha_domination_end_event(
            self,
            total_win=self.win_manager.running_bet_win,
            max_multiplier_reached=self.max_hunt_multiplier,
        )

    def guarantee_alpha_wolves(self):
        """
        Ensure minimum number of ALPHA_WOLF symbols appear on the board.
        Used in Alpha Domination mode.
        """
        conditions = self.get_current_distribution_conditions()
        guaranteed = conditions.get("guaranteed_alpha_wolves", 2)

        # Count existing alpha wolves
        alpha_positions = self.find_special_symbols_on_board("ALPHA_WOLF")
        current_count = len(alpha_positions)

        # Add more if needed
        if current_count < guaranteed:
            needed = guaranteed - current_count
            available_positions = []

            # Find positions without alpha wolves
            for reel_idx, reel in enumerate(self.board):
                for row_idx, symbol in enumerate(reel):
                    if symbol.name != "ALPHA_WOLF":
                        available_positions.append({"reel": reel_idx, "row": row_idx})

            # Randomly select positions to replace
            if available_positions and needed > 0:
                import random
                selected = random.sample(
                    available_positions,
                    min(needed, len(available_positions))
                )

                for pos in selected:
                    self.board[pos["reel"]][pos["row"]] = self.create_alpha_wolf_symbol()
