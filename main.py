"""
Boxing Backtester with Natal Chart Analysis
Entry point.

Usage:
    python main.py                # Full 20-fight backtest with default weights
    python main.py --tune         # Tune weights, then run backtest
    python main.py --fight N      # Run only fight N (1-20)
    python main.py --json         # Print JSON output only
"""

import argparse
import json
import sys

from fights import FIGHTS
from backtester import run_backtest, print_results, DEFAULT_WEIGHTS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Boxing backtester using Swiss Ephemeris natal chart analysis"
    )
    parser.add_argument(
        "--tune",
        action="store_true",
        help="Run staged grid-search tuner to find best weights, then backtest",
    )
    parser.add_argument(
        "--fight",
        type=int,
        metavar="N",
        help="Run only fight number N (1-20) for debugging",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output only (no formatted table)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Select fights to analyze
    if args.fight is not None:
        if args.fight < 1 or args.fight > len(FIGHTS):
            print(f"Error: --fight must be between 1 and {len(FIGHTS)}", file=sys.stderr)
            return 1
        selected_fights = [FIGHTS[args.fight - 1]]
    else:
        selected_fights = FIGHTS

    # Determine weights
    if args.tune:
        from tuner import tune
        weights = tune(selected_fights, verbose=not args.json)
    else:
        weights = DEFAULT_WEIGHTS

    # Run backtest
    summary = run_backtest(selected_fights, weights)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_results(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
