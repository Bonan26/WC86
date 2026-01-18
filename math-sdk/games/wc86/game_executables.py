"""
WC86 - Wolf Club 86
Game Executables - Ways evaluation with Wilds, Howl Chain, Pack Split, Territory
"""

from games.wc86.game_calculations import GameCalculations
from src.calculations.ways import Ways
from games.wc86.game_events import (
    update_hunt_multiplier_event,
    howl_chain_event,
    pack_split_event,
    territory_expand_event,
)


class GameExecutables(GameCalculations):
    """WC86 specific executables for ways wins with special mechanics."""

    def evaluate_ways_board(self):
        """
        Evaluate the board for ways wins with WC86 special mechanics.
        Includes: Hunt Multiplier, Howl Chain, Pack Split processing.
        """
        # First, process Pack Split if ALPHAWOLF is present
        self.process_pack_split()

        # Find and process Howl Chain (adjacent HOWLINGWILDs)
        chain_multiplier = self.process_howl_chain()

        # Calculate ways wins with global multiplier from hunt cascade
        total_multiplier = self.hunt_multiplier * chain_multiplier

        self.win_data = Ways.get_ways_data(
            self.config,
            self.board,
            wild_key="wild",
            global_multiplier=total_multiplier,
            multiplier_key="multiplier",
            multiplier_strategy="global",
        )

        if self.win_data["totalWin"] > 0:
            Ways.record_ways_wins(self)
            self.win_manager.update_spinwin(self.win_data["totalWin"])

        Ways.emit_wayswin_events(self)

    def process_pack_split(self):
        """
        Process Pack Split mechanic when ALPHAWOLF lands.
        Alpha Wolf duplicates to positions on the left.
        """
        alpha_positions = self.find_special_symbols_on_board("ALPHAWOLF")

        for alpha_pos in alpha_positions:
            # Determine split count (weighted random)
            split_count = self.get_pack_split_count()

            if split_count > 1:
                # Get affected positions
                affected = self.get_pack_split_positions(alpha_pos, split_count, self.board)

                if affected:
                    # Apply pack split - replace symbols at affected positions with ALPHAWOLF
                    for pos in affected:
                        self.board[pos["reel"]][pos["row"]] = self.create_alpha_wolf_symbol()

                    # Calculate cumulative multiplier
                    cumulative_mult = split_count

                    # Emit pack split event
                    pack_split_event(
                        self,
                        alpha_position=alpha_pos,
                        split_count=split_count,
                        affected_positions=affected,
                        cumulative_multiplier=cumulative_mult,
                    )

    def process_howl_chain(self):
        """
        Process Howl Chain mechanic for adjacent HOWLINGWILDs.
        Returns the chain multiplier to apply to wins.
        """
        howling_positions = self.find_special_symbols_on_board("HOWLINGWILD")

        if len(howling_positions) < 2:
            return 1

        # Find all connected groups of HOWLINGWILDs
        visited = set()
        chains = []

        for pos in howling_positions:
            pos_key = (pos["reel"], pos["row"])
            if pos_key not in visited:
                # Find all connected wilds starting from this position
                connected = self.find_connected_wilds(pos, self.board, ["HOWLINGWILD"])

                if len(connected) >= 2:
                    chains.append(connected)
                    for c in connected:
                        visited.add((c["reel"], c["row"]))

        if not chains:
            return 1

        # Calculate combined multiplier from all chains
        total_chain_mult = 1

        for chain in chains:
            chain_mult, chain_type = self.calculate_howl_chain_multiplier(chain, self.board)

            # Get individual wild multipliers for event data
            wild_data = []
            for pos in chain:
                symbol = self.board[pos["reel"]][pos["row"]]
                mult = symbol.get_attribute("multiplier") if symbol.check_attribute("multiplier") else 1
                wild_data.append({
                    "reel": pos["reel"],
                    "row": pos["row"],
                    "multiplier": mult,
                })

            # Emit howl chain event
            howl_chain_event(
                self,
                wild_positions=wild_data,
                chain_type=chain_type,
                chain_multiplier=chain_mult,
            )

            total_chain_mult *= chain_mult

        return total_chain_mult

    def find_special_symbols_on_board(self, symbol_name):
        """Find all positions of a specific symbol on the board."""
        positions = []
        for reel_idx, reel in enumerate(self.board):
            for row_idx, symbol in enumerate(reel):
                if symbol.name == symbol_name:
                    positions.append({"reel": reel_idx, "row": row_idx})
        return positions

    def get_pack_split_count(self):
        """
        Determine pack split count based on configured probabilities.
        Returns 1 (no split), 2, 3, or 4.
        """
        import random
        from src.calculations.statistics import get_random_outcome

        # 50% chance of no split
        if random.random() < 0.5:
            return 1

        # If split occurs, determine count
        return get_random_outcome(self.config.pack_split_chances)

    def create_alpha_wolf_symbol(self):
        """Create a new ALPHAWOLF symbol instance."""
        # Use the SDK's symbol_storage to create symbols properly
        symbol = self.symbol_storage.create_symbol("ALPHAWOLF")
        symbol.assign_attribute({"wild": True})
        return symbol

    def process_territory_collection(self):
        """
        Process TERRITORY symbol collection for grid expansion.
        Called during free spins.

        NOTE: Grid expansion temporarily disabled until reelstrips support 8 columns.
        """
        territory_positions = self.find_special_symbols_on_board("TERRITORY")
        collected = len(territory_positions)

        if collected > 0:
            self.territory_collected += collected

            # Grid expansion disabled for now - reelstrips only have 6 columns
            # TODO: Enable once FR_*.csv files have 8 columns
            # new_grid = self.config.check_grid_expansion(
            #     self.territory_collected,
            #     self.current_grid
            # )
            #
            # if new_grid:
            #     previous_grid = self.current_grid
            #     self.expand_grid(new_grid)
            #
            #     territory_expand_event(
            #         self,
            #         previous_grid=previous_grid,
            #         new_grid=new_grid,
            #         territory_count=self.territory_collected,
            #         new_ways_count=self.calculate_ways_count(new_grid),
            #     )

    def expand_grid(self, new_grid):
        """
        Expand the game grid to a new size.
        Updates board dimensions and adds new symbol positions.
        """
        self.current_grid = new_grid
        grid_config = self.config.get_grid_config(new_grid)

        # Update dimensions
        new_reels = grid_config["reels"]
        new_rows = grid_config["rows"]

        # Extend existing reels with new rows
        for reel_idx in range(len(self.board)):
            while len(self.board[reel_idx]) < new_rows:
                # Draw new symbol for extended position
                new_symbol = self.draw_single_symbol(reel_idx)
                self.board[reel_idx].append(new_symbol)

        # Add new reels if needed
        while len(self.board) < new_reels:
            new_reel = []
            for _ in range(new_rows):
                new_symbol = self.draw_single_symbol(len(self.board))
                new_reel.append(new_symbol)
            self.board.append(new_reel)

        # Update config references
        self.config.num_reels = new_reels
        self.config.num_rows = [new_rows] * new_reels

    def draw_single_symbol(self, reel_idx):
        """Draw a single symbol for the specified reel."""
        import random

        reel_name = self.get_current_reel_name()
        reel_strip = self.config.reels.get(reel_name)

        if reel_strip and reel_idx < len(reel_strip):
            # Pick random position from reel strip
            pos = random.randint(0, len(reel_strip[reel_idx]) - 1)
            symbol_name = reel_strip[reel_idx][pos]
            return self.symbol_storage.create_symbol(symbol_name)

        # Fallback - return random low symbol
        low_symbols = ["COCKTAIL", "VIPCARD", "DISCOBALL", "DICE"]
        return self.symbol_storage.create_symbol(random.choice(low_symbols))

    def update_hunt_multiplier(self):
        """
        Update the Hunt Cascade multiplier.
        Called after each cascade (tumble) with wins.
        """
        mult_cap = self.config.get_mult_cap(self.gametype)

        if self.hunt_multiplier < mult_cap:
            self.hunt_multiplier += 1
            self.cascade_count += 1

            # Emit hunt multiplier update event
            update_hunt_multiplier_event(
                self,
                hunt_multiplier=self.hunt_multiplier,
                cascade_count=self.cascade_count,
                mult_cap=mult_cap,
            )

    def execute_tumble_cascade(self):
        """
        Execute the Hunt Cascade (tumble) mechanic.
        Winning symbols explode, new ones fall, multiplier increases.
        """
        while self.win_data["totalWin"] > 0 and not self.wincap_triggered:
            # Update hunt multiplier for this cascade
            self.update_hunt_multiplier()

            # Tumble the board (remove winners, add new symbols)
            self.tumble_game_board()

            # Process territory collection during free spins
            if self.gametype == self.config.freegame_type:
                self.process_territory_collection()

            # Re-evaluate board with new symbols
            self.evaluate_ways_board()

            # Update wins
            self.win_manager.update_gametype_wins(self.gametype)
