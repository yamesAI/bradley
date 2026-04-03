"""
Main backtester: combines event chart + natal analysis to predict fight outcomes.

Weighting logic (tunable):
  - Base: event chart 40%, natal 60%
  - If natal diff strongly favors one side (> threshold): boost natal weight
  - If event diff strongly favors one side (> threshold): boost event weight
  - If both strongly agree: use base weights but flag as high confidence
"""

import json

from ephemeris import get_chart_dict
from event_analysis import analyze_event_chart
from natal_analysis import compare_natal_fighters

DEFAULT_WEIGHTS = {
    # Dignity scores (tuned: domicile strength dominates)
    "domicile": 8,
    "exaltation": 2,
    "detriment": -4,
    "fall": -2,
    "neutral": 0,
    # House scores (tuned: angular strong, cadent very negative)
    "angular": 4,
    "succedent": -1,
    "cadent": -4,
    # Factor weights: temperament (Venus/Jupiter/Saturn) dominates
    "vitality_w": 0.0,
    "alertness_w": 0.0,
    "temperament_w": 4.0,
    # Combination: almost entirely natal, minimal event chart
    "event_weight": 0.05,
    # Dynamic adjustment thresholds
    "natal_trust_threshold": 3.0,
    "event_trust_threshold": 1.0,
    "natal_boost_weight": 0.9,
    "event_boost_weight": 0.8,
}


def _apply_combination_logic(event_result: dict, natal_comparison: dict,
                              weights: dict) -> tuple:
    """
    Combine event and natal scores using dynamic weight adjustment.

    Returns:
        (champion_final, challenger_final, confidence_raw)
        confidence_raw is a raw score difference (not yet a percentage)
    """
    ew_base = weights.get("event_weight", 0.4)
    nw_base = 1.0 - ew_base
    natal_thresh = weights.get("natal_trust_threshold", 2.0)
    event_thresh = weights.get("event_trust_threshold", 2.0)
    natal_boost = weights.get("natal_boost_weight", 0.8)
    event_boost = weights.get("event_boost_weight", 0.6)

    ec = event_result["champion_score"]
    ex = event_result["challenger_score"]
    nc = natal_comparison["champion_bonus"]
    nx = natal_comparison["challenger_bonus"]

    natal_diff = abs(nc - nx)
    event_diff = abs(ec - ex)

    confidence_boost = 1.0
    if natal_diff > natal_thresh and event_diff <= event_thresh:
        ew, nw = 1.0 - natal_boost, natal_boost
    elif event_diff > event_thresh and natal_diff <= natal_thresh:
        ew, nw = event_boost, 1.0 - event_boost
    elif natal_diff > natal_thresh and event_diff > event_thresh:
        ew, nw = ew_base, nw_base
        confidence_boost = 1.2
    else:
        ew, nw = ew_base, nw_base

    champion_final = (ec * ew) + (nc * nw)
    challenger_final = (ex * ew) + (nx * nw)
    raw_diff = abs(champion_final - challenger_final) * confidence_boost
    return champion_final, challenger_final, raw_diff


def _determine_winner(fight: dict, champ_final: float, chall_final: float,
                      conf_raw: float) -> tuple:
    """
    Determine predicted winner name and confidence percentage.

    Returns:
        (predicted_winner_name: str, confidence_pct: float)
    """
    champ_name = fight["champion"]["name"]
    chall_name = fight["challenger"]["name"]

    if champ_final >= chall_final:
        winner = champ_name
    else:
        winner = chall_name

    # Map raw score difference to confidence [50, 99]
    # A difference of 10+ maps to ~95%; 0 maps to 50%
    confidence = 50.0 + min(conf_raw * 2.5, 49.0)
    confidence = max(50.0, min(99.0, confidence))
    return winner, round(confidence, 1)


def analyze_fight(fight: dict, weights: dict = None) -> dict:
    """
    Full analysis pipeline for one fight.

    Returns:
        {
          "fight": str,
          "predicted_winner": str,
          "actual_winner": str,
          "correct": bool,
          "confidence": float,
          "factors": {
            "event_chart": {...},
            "natal_vitality": {...},
            "natal_alertness": {...},
            "natal_temperament": {...},
            "combined": {...}
          }
        }
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    champ = fight["champion"]
    chall = fight["challenger"]
    clat, clon = fight["location"]

    champ_chart = get_chart_dict(
        champ["birth_datetime"], champ["birth_location"][0], champ["birth_location"][1]
    )
    chall_chart = get_chart_dict(
        chall["birth_datetime"], chall["birth_location"][0], chall["birth_location"][1]
    )

    event_result = analyze_event_chart(fight["datetime"], clat, clon, w)
    natal_cmp = compare_natal_fighters(champ_chart, chall_chart, w)

    champ_final, chall_final, conf_raw = _apply_combination_logic(
        event_result, natal_cmp, w
    )
    predicted_winner, confidence = _determine_winner(
        fight, champ_final, chall_final, conf_raw
    )

    correct = predicted_winner == fight["actual_winner"]

    return {
        "fight": fight["fight"],
        "predicted_winner": predicted_winner,
        "actual_winner": fight["actual_winner"],
        "correct": correct,
        "confidence": confidence,
        "factors": {
            "event_chart": {
                "champion": round(event_result["champion_score"], 3),
                "challenger": round(event_result["challenger_score"], 3),
                "dominant": event_result["dominant"],
            },
            "natal_vitality": {
                "champion": round(natal_cmp["champion_vitality"], 3),
                "challenger": round(natal_cmp["challenger_vitality"], 3),
                "dominant": natal_cmp["vitality_dominant"],
            },
            "natal_alertness": {
                "champion": round(natal_cmp["champion_alertness"], 3),
                "challenger": round(natal_cmp["challenger_alertness"], 3),
                "dominant": natal_cmp["alertness_dominant"],
            },
            "natal_temperament": {
                "champion": round(natal_cmp["champion_temperament"], 3),
                "challenger": round(natal_cmp["challenger_temperament"], 3),
                "dominant": natal_cmp["temperament_dominant"],
            },
            "combined": {
                "champion": round(champ_final, 3),
                "challenger": round(chall_final, 3),
            },
        },
    }


def run_backtest(fights: list, weights: dict = None) -> dict:
    """
    Run analysis on all fights and return summary.

    Returns:
        {
          "results": [...],
          "correct": int,
          "total": int,
          "accuracy": float
        }
    """
    results = []
    correct_count = 0
    for fight in fights:
        result = analyze_fight(fight, weights)
        results.append(result)
        if result["correct"]:
            correct_count += 1

    total = len(fights)
    accuracy = (correct_count / total * 100) if total > 0 else 0.0

    return {
        "results": results,
        "correct": correct_count,
        "total": total,
        "accuracy": round(accuracy, 1),
    }


def print_results(summary: dict, output_file: str = "results.json") -> None:
    """Print formatted backtest table and write results.json."""
    results = summary["results"]

    # Header
    print("\n" + "=" * 90)
    print(f"{'BOXING BACKTESTER — NATAL CHART ANALYSIS':^90}")
    print("=" * 90)
    print(
        f"{'Fight':<42} {'Predicted':<20} {'Actual':<20} {'Conf':>5} {'OK':>3}"
    )
    print("-" * 90)

    for r in results:
        fight_label = r["fight"][:41]
        pred = r["predicted_winner"].split()[-1][:19]  # last name
        actual = r["actual_winner"].split()[-1][:19]
        conf = f"{r['confidence']:.1f}%"
        ok = "✓" if r["correct"] else "✗"
        print(f"{fight_label:<42} {pred:<20} {actual:<20} {conf:>5} {ok:>3}")

    print("=" * 90)
    print(
        f"Result: {summary['correct']}/{summary['total']} correct "
        f"({summary['accuracy']}% accuracy)"
    )
    print("=" * 90 + "\n")

    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Full results written to {output_file}")
