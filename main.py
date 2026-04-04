"""
Boxing Backtester with Natal Chart Analysis
Entry point.

Usage:
    python main.py                           # 20-fight local backtest (default weights)
    python main.py --tune                    # Tune weights, then backtest
    python main.py --fight N                 # Run only fight N (1-based)
    python main.py --json                    # JSON output only
    python main.py --source api              # Load 100 fights from OpenBoxing API
    python main.py --source api --sample 50  # Load 50 fights from API
    python main.py --source api --tune       # Tune on API data, then backtest
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
        help="Run only fight number N (1-based, local source only)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output only (no formatted table)",
    )
    parser.add_argument(
        "--source",
        choices=["local", "api"],
        default="local",
        help="Fight data source: 'local' uses fights.py, 'api' fetches from openboxing.org",
    )
    parser.add_argument(
        "--sample",
        type=int,
        metavar="N",
        default=None,
        help="Take first N fights from source (default: all for local, 100 for api)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Load fight data
    if args.source == "api":
        from api_loader import load_api_fights
        n = args.sample if args.sample is not None else 100
        selected_fights = load_api_fights(n=n)
        if not selected_fights:
            print("Error: no valid fights loaded from API", file=sys.stderr)
            return 1
    else:
        # Local source
        if args.fight is not None:
            if args.fight < 1 or args.fight > len(FIGHTS):
                print(
                    f"Error: --fight must be between 1 and {len(FIGHTS)}",
                    file=sys.stderr,
                )
                return 1
            selected_fights = [FIGHTS[args.fight - 1]]
        else:
            selected_fights = FIGHTS
            if args.sample is not None:
                selected_fights = selected_fights[: args.sample]

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
