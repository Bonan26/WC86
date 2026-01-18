"""
WC86 - Wolf Club 86
Game Calculations - Math utilities for dynamic grid and special mechanics
"""

from src.executables.executables import Executables
from games.wc86.game_config import GridSize


class GameCalculations(Executables):
    """WC86 specific calculations for dynamic grid and special features."""

    def calculate_ways_count(self, grid_size=None):
        """
        Calculate the number of ways for current or specified grid size.
        Ways = rows^reels for standard ways calculation.
        """
        if grid_size is None:
            grid_size = getattr(self, "current_grid", GridSize.BASE)

        grid_config = self.config.get_grid_config(grid_size)
        rows = grid_config["rows"]
        reels = grid_config["reels"]

        # Standard ways calculation: each reel contributes 'rows' symbols
        return rows ** reels

    def find_adjacent_positions(self, position, board):
        """
        Find all positions adjacent to the given position (4-directional).
        Used for Howl Chain mechanic.

        Args:
            position: dict with 'reel' and 'row' keys
            board: current game board

        Returns:
            list of adjacent positions that are within board bounds
        """
        reel, row = position["reel"], position["row"]
        adjacent = []

        # 4-directional adjacency (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_reel = reel + dr
            new_row = row + dc

            # Check bounds
            if 0 <= new_reel < len(board) and 0 <= new_row < len(board[new_reel]):
                adjacent.append({"reel": new_reel, "row": new_row})

        return adjacent

    def find_connected_wilds(self, start_position, board, wild_symbols):
        """
        Find all HOWLING_WILD symbols connected to the start position.
        Uses flood-fill algorithm for adjacency detection.

        Args:
            start_position: starting position for search
            board: current game board
            wild_symbols: list of wild symbol names

        Returns:
            list of connected wild positions
        """
        visited = set()
        connected = []
        stack = [start_position]

        while stack:
            pos = stack.pop()
            pos_key = (pos["reel"], pos["row"])

            if pos_key in visited:
                continue

            visited.add(pos_key)

            # Check if this position has a HOWLING_WILD
            symbol = board[pos["reel"]][pos["row"]]
            if symbol.name == "HOWLING_WILD":
                connected.append(pos)

                # Add adjacent positions to stack
                for adj in self.find_adjacent_positions(pos, board):
                    adj_key = (adj["reel"], adj["row"])
                    if adj_key not in visited:
                        stack.append(adj)

        return connected

    def calculate_howl_chain_multiplier(self, wild_positions, board):
        """
        Calculate the combined multiplier from Howl Chain mechanic.

        Rules:
        - 2 adjacent HOWLING_WILDs: ADDITIVE (sum multipliers)
        - 3+ adjacent HOWLING_WILDs: MULTIPLICATIVE (multiply all)

        Args:
            wild_positions: list of connected wild positions
            board: current game board

        Returns:
            tuple: (combined_multiplier, chain_type)
        """
        if len(wild_positions) < 2:
            return 1, "none"

        multipliers = []
        for pos in wild_positions:
            symbol = board[pos["reel"]][pos["row"]]
            mult = symbol.get_attribute("multiplier") if symbol.check_attribute("multiplier") else 1
            multipliers.append(mult)

        if len(wild_positions) == 2:
            # Additive: sum of multipliers
            chain_mult = sum(multipliers)
            return chain_mult, "additive"
        else:
            # Multiplicative: product of multipliers
            chain_mult = 1
            for m in multipliers:
                chain_mult *= m
            return chain_mult, "multiplicative"

    def get_pack_split_positions(self, alpha_position, split_count, board):
        """
        Determine positions affected by Pack Split mechanic.
        Alpha Wolf duplicates to positions on the LEFT.

        Args:
            alpha_position: position of the ALPHA_WOLF that triggered split
            split_count: number of duplicates (2, 3, or 4)
            board: current game board

        Returns:
            list of positions that will receive duplicated Alpha Wolf
        """
        affected = []
        reel = alpha_position["reel"]
        row = alpha_position["row"]

        # Split goes to positions on the left (previous reels)
        for i in range(1, split_count):
            target_reel = reel - i
            if target_reel >= 0 and row < len(board[target_reel]):
                affected.append({"reel": target_reel, "row": row})

        return affected

    def calculate_territory_progress(self, territory_count, current_grid):
        """
        Calculate progress toward next grid expansion.

        Args:
            territory_count: number of TERRITORY symbols collected
            current_grid: current grid size

        Returns:
            dict with progress info
        """
        thresholds = self.config.grid_expansion_thresholds
        grid_order = [GridSize.BASE, GridSize.EXPAND_1, GridSize.EXPAND_2, GridSize.MAX]

        current_idx = grid_order.index(current_grid) if current_grid in grid_order else 0

        # Find next threshold
        next_threshold = None
        next_grid = None

        for threshold, grid in sorted(thresholds.items()):
            grid_idx = grid_order.index(grid)
            if grid_idx > current_idx:
                next_threshold = threshold
                next_grid = grid
                break

        if next_threshold is None:
            # Already at max grid
            return {
                "current_count": territory_count,
                "next_threshold": None,
                "next_grid": None,
                "progress_percent": 100,
                "at_max": True,
            }

        progress = min(100, int((territory_count / next_threshold) * 100))

        return {
            "current_count": territory_count,
            "next_threshold": next_threshold,
            "next_grid": next_grid,
            "progress_percent": progress,
            "at_max": False,
        }
