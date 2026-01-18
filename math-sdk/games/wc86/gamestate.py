"""
WC86 - Wolf Club 86
Game State - Main game logic for basegame, freegame, and alpha domination
"""

from games.wc86.game_override import GameStateOverride
from games.wc86.game_config import GridSize


class GameState(GameStateOverride):
    """
    Main game logic for WC86.

    Game Flow:
    1. Basegame: 6x5 grid, Hunt Cascade with multiplier, scatter triggers Free Spins
    2. Pack Hunt (Free Spins): Multiplier persists, Territory expands grid, retriggers
    3. Alpha Domination: 8x8 grid, starts at x5, guaranteed Alpha Wolves
    """

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        """
        Execute a single basegame spin.
        Includes Hunt Cascade (tumble) mechanic with increasing multiplier.
        """
        self.reset_seed(sim)
        self.repeat = True

        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=True)

            # Evaluate initial board
            self.evaluate_ways_board()

            # Execute Hunt Cascade (tumble until no more wins)
            if self.win_data["totalWin"] > 0:
                self.execute_tumble_cascade()

            self.win_manager.update_gametype_wins(self.gametype)

            # Check for Free Spin trigger (MOON_SCATTER)
            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        """
        Execute Pack Hunt (Free Spins) mode.

        Features:
        - Hunt Multiplier persists between spins
        - Territory symbols expand the grid (6x5 → 7x6 → 8x7 → 8x8)
        - Retriggers add more spins
        - Higher multiplier cap than basegame
        """
        self.reset_fs_spin()

        # Initialize free spin specific state
        self.territory_collected = 0
        self.current_grid = GridSize.BASE

        # Get starting multiplier from conditions (pack_hunt_plus starts at x3)
        conditions = self.get_current_distribution_conditions()
        if "starting_multiplier" in conditions:
            self.hunt_multiplier = conditions["starting_multiplier"]
        else:
            # Carry over multiplier from basegame trigger spin
            pass

        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board(emit_event=True)

            # Process Territory collection first (for grid expansion)
            self.process_territory_collection()

            # Evaluate board with current multiplier
            self.evaluate_ways_board()

            # Execute Hunt Cascade
            if self.win_data["totalWin"] > 0:
                self.execute_tumble_cascade()

            # Check for retrigger
            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

            # Track max multiplier
            if self.hunt_multiplier > self.max_hunt_multiplier:
                self.max_hunt_multiplier = self.hunt_multiplier

            self.win_manager.update_gametype_wins(self.gametype)

        self.end_freespin()

    def run_alpha_domination(self) -> None:
        """
        Execute Alpha Domination super bonus mode.

        Features:
        - Fixed 8x8 grid (262,144 ways)
        - Starting multiplier of x5
        - Multiplier cap of 500
        - Guaranteed Alpha Wolves per spin
        - Continues until no more wins (single "mega spin")
        """
        # Enter Alpha Domination mode
        self.enter_alpha_domination()

        # Draw initial 8x8 board
        self.draw_board(emit_event=True)

        # Guarantee Alpha Wolves on the board
        self.guarantee_alpha_wolves()

        # Evaluate initial board
        self.evaluate_ways_board()

        # Execute Hunt Cascade until no more wins or wincap
        while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
            # Update multiplier
            self.update_hunt_multiplier()

            # Track max
            if self.hunt_multiplier > self.max_hunt_multiplier:
                self.max_hunt_multiplier = self.hunt_multiplier

            # Tumble board
            self.tumble_game_board()

            # Guarantee Alpha Wolves again after tumble
            self.guarantee_alpha_wolves()

            # Re-evaluate
            self.evaluate_ways_board()

            self.win_manager.update_gametype_wins(self.gametype)

        # End Alpha Domination
        self.end_alpha_domination()

    def run_spin_for_mode(self, sim: int, bet_mode_name: str, simulation_seed=None) -> None:
        """
        Execute a spin for a specific bet mode.
        Routes to appropriate game mode based on bet mode name.
        """
        self.reset_seed(sim)
        self.repeat = True

        while self.repeat:
            self.reset_book()

            if bet_mode_name == "alpha_domination":
                # Alpha Domination super bonus
                self.run_alpha_domination()
                self.evaluate_finalwin()
                self.repeat = False

            elif bet_mode_name in ["pack_hunt", "pack_hunt_plus"]:
                # Buy bonus - go directly to free spins
                self.draw_board(emit_event=True)

                # Evaluate initial board for any wins before FS
                self.evaluate_ways_board()
                if self.win_data["totalWin"] > 0:
                    self.execute_tumble_cascade()

                self.win_manager.update_gametype_wins(self.gametype)

                # Set up free spins (bought, so guaranteed trigger)
                scatter_count = 3  # Minimum trigger
                self.tot_fs = self.config.freespin_triggers[self.config.basegame_type][scatter_count]

                # Emit fake scatter trigger for animation
                from game_events import freespin_trigger_wc86_event
                freespin_trigger_wc86_event(
                    self,
                    scatter_positions=[],  # No actual scatters needed
                    total_spins=self.tot_fs,
                    is_retrigger=False,
                )

                self.run_freespin()
                self.evaluate_finalwin()
                self.check_repeat()

            else:
                # Normal basegame spin
                self.draw_board(emit_event=True)
                self.evaluate_ways_board()

                if self.win_data["totalWin"] > 0:
                    self.execute_tumble_cascade()

                self.win_manager.update_gametype_wins(self.gametype)

                if self.check_fs_condition() and self.check_freespin_entry():
                    self.run_freespin_from_base()

                self.evaluate_finalwin()
                self.check_repeat()

        self.imprint_wins()

    def execute_tumble_cascade(self):
        """
        Execute the Hunt Cascade (tumble) mechanic.
        Override to handle WC86 specific cascade behavior.
        """
        while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
            # Increment hunt multiplier
            mult_cap = self.config.get_mult_cap(self.gametype)

            if self.hunt_multiplier < mult_cap:
                self.hunt_multiplier += 1
                self.cascade_count += 1

                # Emit hunt multiplier update
                from game_events import update_hunt_multiplier_event
                update_hunt_multiplier_event(
                    self,
                    hunt_multiplier=self.hunt_multiplier,
                    cascade_count=self.cascade_count,
                    mult_cap=mult_cap,
                )

            # Tumble the board
            self.tumble_game_board()

            # Process territory during free spins
            if self.gametype == self.config.freegame_type:
                self.process_territory_collection()

            # Re-evaluate with new symbols
            self.evaluate_ways_board()

            self.win_manager.update_gametype_wins(self.gametype)

    def check_repeat(self):
        """
        Check if the spin should be repeated due to unmet conditions.
        """
        # Check parent conditions
        self.check_game_repeat()

        # WC86 specific checks
        conditions = self.get_current_distribution_conditions()

        # Check wincap requirement
        if conditions.get("force_wincap", False):
            if self.final_win < self.config.wincap * 0.95:
                self.repeat = True

        # Check freegame requirement
        if conditions.get("force_freegame", False):
            if self.win_manager.freegame_wins == 0:
                self.repeat = True
