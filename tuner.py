"""
Staged grid-search tuner to maximize backtest accuracy.

Strategy:
  Stage 1: Search dignity score values (domicile/exaltation/detriment/fall)
  Stage 2: Search house scores (angular/succedent/cadent)
  Stage 3: Search natal factor weights (vitality/alertness/temperament)
  Stage 4: Search combination weights (event_weight)
  Stage 5: Search dynamic threshold weights

Each stage fixes the previous best values and varies the current parameters.
Chart lookups are memoized in ephemeris.py — the tuner reuses cached results.
"""

import itertools

from backtester import DEFAULT_WEIGHTS, run_backtest


def _accuracy(fights: list, weights: dict) -> tuple:
    """Return (accuracy_pct, avg_confidence_when_correct) for tie-breaking."""
    summary = run_backtest(fights, weights)
    correct = [r for r in summary["results"] if r["correct"]]
    avg_conf = sum(r["confidence"] for r in correct) / len(correct) if correct else 0.0
    return summary["accuracy"], avg_conf


def _search(fights: list, base_weights: dict, param_grid: dict,
            verbose: bool, stage_name: str) -> dict:
    """
    Grid search over param_grid, starting from base_weights.
    Returns best weights dict found.
    """
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    best_weights = dict(base_weights)
    best_acc, best_conf = _accuracy(fights, best_weights)

    combos = list(itertools.product(*values))
    if verbose:
        print(f"\n[Stage: {stage_name}] Testing {len(combos)} combinations...")

    for combo in combos:
        candidate = dict(base_weights)
        for k, v in zip(keys, combo):
            candidate[k] = v
        # natal_weight is always 1 - event_weight
        if "event_weight" in candidate:
            candidate["natal_weight"] = 1.0 - candidate["event_weight"]
        acc, conf = _accuracy(fights, candidate)
        if (acc, conf) > (best_acc, best_conf):
            best_acc, best_conf = acc, conf
            best_weights = dict(candidate)

    if verbose:
        print(f"  Best accuracy: {best_acc:.1f}% | conf: {best_conf:.1f}")
        for k in keys:
            print(f"    {k} = {best_weights[k]}")

    return best_weights


def tune(fights: list, verbose: bool = True) -> dict:
    """
    Run staged grid search to find best weights for the given fight list.

    Returns:
        best_weights dict
    """
    if verbose:
        print("\n=== TUNER: Staged Grid Search ===")

    weights = dict(DEFAULT_WEIGHTS)

    # Stage 1: Dignity score values
    # Domicile range extended to 8 to allow strong home-sign emphasis
    weights = _search(fights, weights, {
        "domicile":   [3, 4, 5, 6, 7, 8],
        "exaltation": [1, 2, 3, 4, 5],
        "detriment":  [-6, -5, -4, -3],
        "fall":       [-5, -4, -3, -2],
    }, verbose, "Dignity scores")

    # Stage 2: House scores
    # Succedent can be negative (non-traditional but empirically useful)
    weights = _search(fights, weights, {
        "angular":   [2, 3, 4, 5],
        "succedent": [-2, -1, 0, 1, 2],
        "cadent":    [-4, -3, -2, -1, 0],
    }, verbose, "House scores")

    # Stage 3: Natal factor weights (including 0.0 to allow dropping a factor)
    weights = _search(fights, weights, {
        "vitality_w":    [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
        "alertness_w":   [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
        "temperament_w": [0.5, 1.0, 1.5, 2.0, 3.0, 4.0],
    }, verbose, "Factor weights")

    # Stage 4: Event vs natal combination weight
    # Near-zero event weights allowed since natal dominates
    weights = _search(fights, weights, {
        "event_weight": [0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5],
    }, verbose, "Event/natal blend")

    # Stage 5: Dynamic threshold values
    weights = _search(fights, weights, {
        "natal_trust_threshold": [1.0, 2.0, 3.0, 5.0, 10.0],
        "event_trust_threshold": [1.0, 2.0, 3.0, 5.0, 10.0],
    }, verbose, "Trust thresholds")

    # Stage 6: Boost weights for confident signals
    weights = _search(fights, weights, {
        "natal_boost_weight": [0.6, 0.7, 0.8, 0.9, 1.0],
        "event_boost_weight": [0.5, 0.6, 0.7, 0.8],
    }, verbose, "Boost weights")

    final_acc, _ = _accuracy(fights, weights)
    if verbose:
        print(f"\n=== TUNER COMPLETE: Best accuracy = {final_acc:.1f}% ===")
        print("Best weights:")
        for k, v in weights.items():
            if k != "neutral":
                print(f"  {k} = {v}")

    return weights
