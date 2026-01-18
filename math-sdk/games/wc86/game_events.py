"""
WC86 - Wolf Club 86
Custom Game Events - Book events for ELI to consume
"""

from src.events.events import *


def update_hunt_multiplier_event(gamestate, hunt_multiplier, cascade_count, mult_cap):
    """
    Emit event when Hunt Cascade multiplier increases.

    Event data format (for ELI):
    {
        "type": "updateHuntMultiplier",
        "index": int,
        "huntMultiplier": int,      # Current multiplier value
        "cascadeCount": int,        # Number of cascades so far
        "multCap": int              # Maximum multiplier allowed
    }
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "updateHuntMultiplier",
        "huntMultiplier": int(hunt_multiplier),
        "cascadeCount": int(cascade_count),
        "multCap": int(mult_cap),
    }
    gamestate.book.add_event(event)


def pack_split_event(gamestate, alpha_position, split_count, affected_positions, cumulative_multiplier):
    """
    Emit event when Alpha Wolf triggers Pack Split.
    Alpha Wolf duplicates to positions on the left.

    Event data format (for ELI):
    {
        "type": "packSplit",
        "index": int,
        "alphaPosition": {reel: int, row: int},    # Original alpha position
        "splitCount": int,                          # 2, 3, or 4
        "affectedPositions": [{reel, row}, ...],   # Positions receiving duplicates
        "cumulativeMultiplier": int                 # x2, x3, or x4
    }
    """
    # Adjust positions for padding if needed
    if gamestate.config.include_padding:
        adjusted_alpha = {
            "reel": alpha_position["reel"],
            "row": alpha_position["row"] + 1,
        }
        adjusted_affected = [
            {"reel": pos["reel"], "row": pos["row"] + 1}
            for pos in affected_positions
        ]
    else:
        adjusted_alpha = alpha_position
        adjusted_affected = affected_positions

    event = {
        "index": len(gamestate.book.events),
        "type": "packSplit",
        "alphaPosition": adjusted_alpha,
        "splitCount": int(split_count),
        "affectedPositions": adjusted_affected,
        "cumulativeMultiplier": int(cumulative_multiplier),
    }
    gamestate.book.add_event(event)


def howl_chain_event(gamestate, wild_positions, chain_type, chain_multiplier):
    """
    Emit event when Howling Wilds form a chain (2+ adjacent).
    2 wilds = additive, 3+ wilds = multiplicative.

    Event data format (for ELI):
    {
        "type": "howlChain",
        "index": int,
        "wildPositions": [{reel, row, multiplier}, ...],  # All connected wilds
        "chainType": "additive" | "multiplicative",       # How multipliers combine
        "chainMultiplier": int                            # Combined multiplier value
    }
    """
    # Adjust positions for padding if needed
    if gamestate.config.include_padding:
        adjusted_positions = [
            {
                "reel": pos["reel"],
                "row": pos["row"] + 1,
                "multiplier": pos["multiplier"],
            }
            for pos in wild_positions
        ]
    else:
        adjusted_positions = wild_positions

    event = {
        "index": len(gamestate.book.events),
        "type": "howlChain",
        "wildPositions": adjusted_positions,
        "chainType": chain_type,
        "chainMultiplier": int(chain_multiplier),
    }
    gamestate.book.add_event(event)


def territory_expand_event(gamestate, previous_grid, new_grid, territory_count, new_ways_count):
    """
    Emit event when grid expands due to Territory symbol collection.

    Event data format (for ELI):
    {
        "type": "territoryExpand",
        "index": int,
        "previousGrid": "6x5" | "7x6" | "8x7",    # Grid before expansion
        "newGrid": "7x6" | "8x7" | "8x8",         # Grid after expansion
        "territoryCount": int,                     # Total territories collected
        "newWaysCount": int                        # New number of ways
    }
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "territoryExpand",
        "previousGrid": previous_grid,
        "newGrid": new_grid,
        "territoryCount": int(territory_count),
        "newWaysCount": int(new_ways_count),
    }
    gamestate.book.add_event(event)


def alpha_domination_start_event(gamestate, starting_multiplier, mult_cap, guaranteed_alpha_wolves):
    """
    Emit event when Alpha Domination super bonus starts.

    Event data format (for ELI):
    {
        "type": "alphaDominationStart",
        "index": int,
        "startingMultiplier": int,       # Minimum 5
        "multCap": int,                  # 500
        "guaranteedAlphaWolves": int     # Number of guaranteed Alpha Wolves per spin
    }
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "alphaDominationStart",
        "startingMultiplier": int(starting_multiplier),
        "multCap": int(mult_cap),
        "guaranteedAlphaWolves": int(guaranteed_alpha_wolves),
    }
    gamestate.book.add_event(event)


def alpha_domination_end_event(gamestate, total_win, max_multiplier_reached):
    """
    Emit event when Alpha Domination super bonus ends.

    Event data format (for ELI):
    {
        "type": "alphaDominationEnd",
        "index": int,
        "totalWin": int,                 # Total win from Alpha Domination
        "maxMultiplierReached": int,     # Highest multiplier achieved
        "winLevel": str                  # "big", "super", "mega", "epic", "max"
    }
    """
    win_level = gamestate.config.get_win_level(total_win, "endFeature")

    event = {
        "index": len(gamestate.book.events),
        "type": "alphaDominationEnd",
        "totalWin": int(min(total_win, gamestate.config.wincap) * 100),
        "maxMultiplierReached": int(max_multiplier_reached),
        "winLevel": win_level,
    }
    gamestate.book.add_event(event)


def reveal_wc86_event(gamestate):
    """
    Extended reveal event for WC86 with additional grid info.

    Event data format (for ELI):
    {
        "type": "reveal",
        "index": int,
        "board": [[{name, wild?, scatter?, multiplier?}, ...], ...],
        "gameType": "basegame" | "freegame" | "alphaDomination",
        "currentGrid": "6x5" | "7x6" | "8x7" | "8x8",
        "huntMultiplier": int,
        "territoryCollected": int,
        "paddingPositions": [int, ...],
        "anticipation": [int, ...]
    }
    """
    board_client = []
    special_attributes = list(gamestate.config.special_symbols.keys())

    for reel_idx, reel in enumerate(gamestate.board):
        board_client.append([])
        for row_idx, symbol in enumerate(reel):
            sym_data = json_ready_sym(symbol, special_attributes)

            # Add multiplier for HOWLING_WILD
            if symbol.name == "HOWLING_WILD" and symbol.check_attribute("multiplier"):
                sym_data["multiplier"] = symbol.get_attribute("multiplier")

            board_client[reel_idx].append(sym_data)

    # Add padding symbols if configured
    if gamestate.config.include_padding:
        for reel_idx in range(len(board_client)):
            top_sym = json_ready_sym(gamestate.top_symbols[reel_idx], special_attributes)
            bottom_sym = json_ready_sym(gamestate.bottom_symbols[reel_idx], special_attributes)
            board_client[reel_idx] = [top_sym] + board_client[reel_idx] + [bottom_sym]

    event = {
        "index": len(gamestate.book.events),
        "type": "reveal",
        "board": board_client,
        "gameType": gamestate.gametype,
        "currentGrid": getattr(gamestate, "current_grid", "6x5"),
        "huntMultiplier": int(getattr(gamestate, "hunt_multiplier", 1)),
        "territoryCollected": int(getattr(gamestate, "territory_collected", 0)),
        "paddingPositions": gamestate.reel_positions,
        "anticipation": gamestate.anticipation,
    }
    gamestate.book.add_event(event)


def freespin_trigger_wc86_event(gamestate, scatter_positions, total_spins, is_retrigger=False):
    """
    WC86 specific free spin trigger event.

    Event data format (for ELI):
    {
        "type": "freeSpinTrigger",
        "index": int,
        "scatterCount": int,
        "scatterPositions": [{reel, row}, ...],
        "totalSpins": int,
        "isRetrigger": bool
    }
    """
    # Adjust positions for padding if needed
    if gamestate.config.include_padding:
        adjusted_positions = [
            {"reel": pos["reel"], "row": pos["row"] + 1}
            for pos in scatter_positions
        ]
    else:
        adjusted_positions = scatter_positions

    event = {
        "index": len(gamestate.book.events),
        "type": "freeSpinTrigger",
        "scatterCount": len(scatter_positions),
        "scatterPositions": adjusted_positions,
        "totalSpins": int(total_spins),
        "isRetrigger": is_retrigger,
    }
    gamestate.book.add_event(event)


def freespin_end_wc86_event(gamestate):
    """
    WC86 specific free spin end event with additional stats.

    Event data format (for ELI):
    {
        "type": "freeSpinEnd",
        "index": int,
        "totalWin": int,
        "spinCount": int,
        "maxMultiplierReached": int,
        "winLevel": str
    }
    """
    win_level = gamestate.config.get_win_level(gamestate.win_manager.freegame_wins, "endFeature")

    event = {
        "index": len(gamestate.book.events),
        "type": "freeSpinEnd",
        "totalWin": int(min(gamestate.win_manager.freegame_wins, gamestate.config.wincap) * 100),
        "spinCount": int(gamestate.fs),
        "maxMultiplierReached": int(getattr(gamestate, "max_hunt_multiplier", 1)),
        "winLevel": win_level,
    }
    gamestate.book.add_event(event)
