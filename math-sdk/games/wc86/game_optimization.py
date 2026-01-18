"""
WC86 - Wolf Club 86
Optimization Setup - Rust optimization configuration for 4 bet modes
"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    ConstructFenceBias,
    verify_optimization_input,
)


class OptimizationSetup:
    """
    WC86 optimization setup for all 4 bet modes:
    - base: Normal play (1.0x cost)
    - pack_hunt: Buy Free Spins (75x cost)
    - pack_hunt_plus: Buy FS with x3 start (150x cost)
    - alpha_domination: Super bonus 8x8 (500x cost)
    """

    def __init__(self, game_config):
        self.game_config = game_config

        # Get wincaps for each bet mode
        wincaps = {}
        for bm in game_config.bet_modes:
            wincaps[bm.get_name()] = bm.get_wincap()

        self.game_config.opt_params = {
            # BASE MODE - Normal play
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.005,  # 0.5% contribution from wincap hits
                        av_win=wincaps["base"],
                        search_conditions=wincaps["base"]
                    ).return_dict(),
                    "0": ConstructConditions(
                        rtp=0,
                        av_win=0,
                        search_conditions=0
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.45,  # 45% of RTP from free games
                        hr=130,    # ~1 in 130 trigger rate
                        search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        hr=3.2,    # ~31% hit rate
                        rtp=0.51   # 51% of RTP from basegame
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    # Basegame scaling - boost small wins
                    {
                        "criteria": "basegame",
                        "scale_factor": 1.3,
                        "win_range": (0.5, 2),
                        "probability": 1.0,
                    },
                    # Basegame - slight boost medium wins
                    {
                        "criteria": "basegame",
                        "scale_factor": 1.1,
                        "win_range": (5, 15),
                        "probability": 1.0,
                    },
                    # Freegame - reduce medium wins for volatility
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.85,
                        "win_range": (500, 1500),
                        "probability": 1.0,
                    },
                    # Freegame - boost big wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.25,
                        "win_range": (5000, wincaps["base"]),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=15000,
                    min_m2m=3,
                    max_m2m=10,
                    pmb_rtp=1.0,
                    sim_trials=10000,
                    test_spins=[50, 100, 250, 500],
                    test_weights=[0.2, 0.3, 0.3, 0.2],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(1.0, 4.0)],
                    bias_weights=[0.35],
                ).return_dict(),
            },

            # PACK HUNT - Buy Free Spins (75x)
            "pack_hunt": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.008,
                        av_win=wincaps["pack_hunt"],
                        search_conditions=wincaps["pack_hunt"]
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.957,  # Almost all RTP from freegame
                        hr="x"      # 100% trigger (bought)
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    # Reduce small wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.9,
                        "win_range": (10, 50),
                        "probability": 1.0,
                    },
                    # Boost medium-high wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.15,
                        "win_range": (200, 500),
                        "probability": 1.0,
                    },
                    # Reduce upper-medium for volatility
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.8,
                        "win_range": (1000, 3000),
                        "probability": 1.0,
                    },
                    # Boost big wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.3,
                        "win_range": (8000, wincaps["pack_hunt"]),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=12000,
                    min_m2m=4,
                    max_m2m=12,
                    pmb_rtp=1.0,
                    sim_trials=8000,
                    test_spins=[10, 20, 50, 100],
                    test_weights=[0.4, 0.3, 0.2, 0.1],
                    score_type="rtp",
                ).return_dict(),
            },

            # PACK HUNT PLUS - Buy FS with x3 start (150x)
            "pack_hunt_plus": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01,
                        av_win=wincaps["pack_hunt_plus"],
                        search_conditions=wincaps["pack_hunt_plus"]
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.955,  # Almost all RTP from freegame
                        hr="x"      # 100% trigger (bought)
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    # Starting at x3 means wins are naturally higher
                    # Reduce low wins more aggressively
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.85,
                        "win_range": (30, 100),
                        "probability": 1.0,
                    },
                    # Boost medium wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.2,
                        "win_range": (300, 800),
                        "probability": 1.0,
                    },
                    # Reduce upper-medium for volatility
                    {
                        "criteria": "freegame",
                        "scale_factor": 0.75,
                        "win_range": (1500, 4000),
                        "probability": 1.0,
                    },
                    # Boost mega wins
                    {
                        "criteria": "freegame",
                        "scale_factor": 1.35,
                        "win_range": (10000, wincaps["pack_hunt_plus"]),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=12000,
                    min_m2m=5,
                    max_m2m=15,
                    pmb_rtp=1.0,
                    sim_trials=8000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.5, 0.3, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },

            # ALPHA DOMINATION - Super Bonus 8x8 (500x)
            "alpha_domination": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.015,
                        av_win=wincaps["alpha_domination"],
                        search_conditions=wincaps["alpha_domination"]
                    ).return_dict(),
                    "alpha_domination": ConstructConditions(
                        rtp=0.95,   # 95% RTP target for this mode
                        hr="x"      # 100% (bought mode)
                    ).return_dict(),
                },
                "scaling": ConstructScaling([
                    # 8x8 with x5 start and guaranteed alphas = big swings
                    # Reduce low outcomes
                    {
                        "criteria": "alpha_domination",
                        "scale_factor": 0.7,
                        "win_range": (50, 200),
                        "probability": 1.0,
                    },
                    # Slight boost medium
                    {
                        "criteria": "alpha_domination",
                        "scale_factor": 1.1,
                        "win_range": (500, 1500),
                        "probability": 1.0,
                    },
                    # Reduce upper-medium
                    {
                        "criteria": "alpha_domination",
                        "scale_factor": 0.65,
                        "win_range": (3000, 10000),
                        "probability": 1.0,
                    },
                    # Massive boost for max wins
                    {
                        "criteria": "alpha_domination",
                        "scale_factor": 1.5,
                        "win_range": (20000, wincaps["alpha_domination"]),
                        "probability": 1.0,
                    },
                ]).return_dict(),
                "parameters": ConstructParameters(
                    num_show=3000,
                    num_per_fence=8000,
                    min_m2m=6,
                    max_m2m=20,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[5, 10, 20],
                    test_weights=[0.6, 0.3, 0.1],
                    score_type="rtp",
                ).return_dict(),
            },
        }

        # Verify all optimization parameters are valid
        verify_optimization_input(self.game_config, self.game_config.opt_params)
