"""
WC86 - Wolf Club 86
Main Entry Point - Run simulations, optimization, and analysis

Usage:
    python run.py --mode PACK --sims 500000
    python run.py --optimize
    python run.py --export-config
    python run.py --analysis
"""

import argparse
from games.wc86.gamestate import GameState
from games.wc86.game_config import GameConfig, VolatilityMode
from games.wc86.game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="WC86 - Wolf Club 86 Math Engine")

    parser.add_argument(
        "--mode",
        type=str,
        choices=["LONE_WOLF", "PACK", "ALPHA"],
        default="PACK",
        help="Volatility mode (default: PACK)"
    )

    parser.add_argument(
        "--sims",
        type=int,
        default=100000,
        help="Number of simulations to run (default: 100000)"
    )

    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run Rust optimization after simulations"
    )

    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Generate stat sheet analysis"
    )

    parser.add_argument(
        "--export-config",
        action="store_true",
        help="Export RGS configuration files"
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Run format verification tests"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of Python threads (default: 10)"
    )

    parser.add_argument(
        "--rust-threads",
        type=int,
        default=20,
        help="Number of Rust threads for optimization (default: 20)"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=50000,
        help="Batch size for simulations (default: 50000)"
    )

    parser.add_argument(
        "--no-compression",
        action="store_true",
        help="Disable compression for book files"
    )

    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable profiling"
    )

    parser.add_argument(
        "--bet-modes",
        type=str,
        nargs="+",
        default=["base", "pack_hunt", "pack_hunt_plus", "alpha_domination"],
        help="Bet modes to simulate (default: all)"
    )

    return parser.parse_args()


def get_volatility_mode(mode_str):
    """Convert string to VolatilityMode enum."""
    modes = {
        "LONE_WOLF": VolatilityMode.LONE_WOLF,
        "PACK": VolatilityMode.PACK,
        "ALPHA": VolatilityMode.ALPHA,
    }
    return modes.get(mode_str, VolatilityMode.PACK)


def main():
    """Main entry point for WC86 math engine."""
    args = parse_args()

    # Configuration
    volatility_mode = get_volatility_mode(args.mode)
    num_threads = args.threads
    rust_threads = args.rust_threads
    batching_size = args.batch_size
    compression = not args.no_compression
    profiling = args.profile

    print(f"\n{'='*60}")
    print(f"WC86 - Wolf Club 86 - Math Engine")
    print(f"{'='*60}")
    print(f"Volatility Mode: {args.mode}")
    print(f"RTP Target: {96.8 if args.mode == 'LONE_WOLF' else 96.5 if args.mode == 'PACK' else 96.2}%")
    print(f"Max Win: {10000 if args.mode == 'LONE_WOLF' else 25000 if args.mode == 'PACK' else 50000}x")
    print(f"{'='*60}\n")

    # Initialize config and gamestate
    config = GameConfig(volatility_mode=volatility_mode)
    gamestate = GameState(config)

    # Setup simulation counts per bet mode
    num_sim_args = {}
    for mode in args.bet_modes:
        # Alpha domination needs fewer sims (expensive mode)
        if mode == "alpha_domination":
            num_sim_args[mode] = max(args.sims // 10, 10000)
        else:
            num_sim_args[mode] = args.sims

    print(f"Simulation counts: {num_sim_args}")

    # Determine what to run
    run_sims = args.sims > 0
    run_optimization = args.optimize
    run_analysis = args.analysis
    run_format_checks = args.verify
    export_config = args.export_config

    # Initialize optimization if needed
    if run_optimization or run_analysis:
        optimization_setup = OptimizationSetup(config)

    # Run simulations
    if run_sims:
        print(f"\n[1/4] Running {sum(num_sim_args.values()):,} simulations...")
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )
        print("Simulations complete!")

    # Generate initial configs
    if export_config or run_sims:
        print("\n[2/4] Generating RGS configuration files...")
        generate_configs(gamestate)
        print("Configs generated!")

    # Run optimization
    if run_optimization:
        print(f"\n[3/4] Running Rust optimization on {args.bet_modes}...")
        OptimizationExecution().run_all_modes(config, args.bet_modes, rust_threads)
        # Regenerate configs after optimization
        generate_configs(gamestate)
        print("Optimization complete!")

    # Run analysis
    if run_analysis:
        print("\n[4/4] Generating stat sheet analysis...")
        custom_keys = [
            {"symbol": "scatter"},
            {"symbol": "ALPHA_WOLF"},
            {"symbol": "HOWLING_WILD"},
            {"symbol": "TERRITORY"},
        ]
        create_stat_sheet(gamestate, custom_keys=custom_keys)
        print("Analysis complete!")

    # Run format verification
    if run_format_checks:
        print("\n[Verification] Running RGS format checks...")
        execute_all_tests(config)
        print("Verification complete!")

    print(f"\n{'='*60}")
    print("WC86 Math Engine - Complete")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
