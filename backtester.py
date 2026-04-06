"""
Main backtester: combines event chart + natal analysis to predict fight outcomes.

Weighting logic (tunable):
  - Base: event chart 40%, natal 60%
  - If natal diff strongly favors one side (> threshold): boost natal weight
  - If event diff strongly favors one side (> threshold): boost event weight
  - If both strongly agree: use base weights but flag as high confidence
"""

import json

from ephemeris import get_chart_dict, get_horary_house_cusps
from event_analysis import analyze_event_chart
from natal_analysis import compare_natal_fighters, compare_natal_in_horary, analyze_natal_in_horary
from dignities import dignity_score
from natal_analysis import house_score

DEFAULT_WEIGHTS = {
    # Dignity scores — tuned for horary-placement methodology
    "domicile": 8,
    "exaltation": 5,
    "detriment": -3,
    "fall": -3,
    "neutral": 0,
    # House scores — angular strongly positive, succedent/cadent negative
    "angular": 5,
    "succedent": -2,
    "cadent": -2,
    # Factor weights — temperament (Venus/Jupiter/Saturn) dominates; alertness minor
    "vitality_w": 0.0,
    "alertness_w": 0.25,
    "temperament_w": 4.0,
    # Combination: equal horary-event and natal-in-horary blend
    "event_weight": 0.5,
    # Dynamic adjustment thresholds
    "natal_trust_threshold": 2.0,
    "event_trust_threshold": 5.0,
    "natal_boost_weight": 1.0,
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

    # Natal charts: birthdate only, fixed location (sign positions only)
    champ_chart = get_chart_dict(champ["birth_datetime"], 0.0, 0.0)
    chall_chart = get_chart_dict(chall["birth_datetime"], 0.0, 0.0)

    # Horary house cusps from fight venue + bell time
    horary_cusps = get_horary_house_cusps(fight["datetime"], clat, clon)

    event_result = analyze_event_chart(fight["datetime"], clat, clon, w)
    natal_cmp = compare_natal_in_horary(champ_chart, chall_chart, horary_cusps, w)

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


def analyze_fight_live(
    fighter1_name: str, fighter1_birthdate: str,
    fighter2_name: str, fighter2_birthdate: str,
    venue_datetime: str,
    venue_lat: float, venue_lon: float,
    weights: dict = None,
) -> dict:
    """
    On-demand fight analysis for the web UI.

    Uses the horary methodology: natal planets placed in horary chart houses.
    Birth time is not needed — birthdate only (noon UTC is used).

    Args:
        fighter1_name: display name for fighter 1
        fighter1_birthdate: "YYYY-MM-DD"
        fighter2_name: display name for fighter 2
        fighter2_birthdate: "YYYY-MM-DD"
        venue_datetime: ISO 8601 with offset e.g. "2024-11-09T21:00:00-08:00"
        venue_lat: venue latitude
        venue_lon: venue longitude
        weights: optional scoring overrides

    Returns:
        Dict with prediction, confidence, and full factor breakdown.
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    # Natal charts: noon UTC, equator (birth location irrelevant — signs only)
    f1_birth_dt = fighter1_birthdate + "T12:00:00+00:00"
    f2_birth_dt = fighter2_birthdate + "T12:00:00+00:00"
    f1_chart = get_chart_dict(f1_birth_dt, 0.0, 0.0)
    f2_chart = get_chart_dict(f2_birth_dt, 0.0, 0.0)

    # Horary house cusps from fight venue + bell time
    horary_cusps = get_horary_house_cusps(venue_datetime, venue_lat, venue_lon)

    # Place each fighter's natal planets in the horary houses
    from ephemeris import place_in_houses
    f1_house_map = {p["planet"]: place_in_houses(p["longitude"], horary_cusps)
                    for p in f1_chart["planets"]}
    f2_house_map = {p["planet"]: place_in_houses(p["longitude"], horary_cusps)
                    for p in f2_chart["planets"]}

    # Score each fighter's natal planets using horary house placement
    f1_scores = analyze_natal_in_horary(f1_chart, f1_house_map, w)
    f2_scores = analyze_natal_in_horary(f2_chart, f2_house_map, w)

    # Secondary: horary chart's own planet polarity (champion=1-6, challenger=7-12)
    # (minor signal, weighted at event_weight)
    event_result = analyze_event_chart(venue_datetime, venue_lat, venue_lon, w)

    # Build natal_cmp dict for combination logic (fighter1 = "champion" slot)
    natal_cmp = {
        "champion_bonus": f1_scores["total"],
        "challenger_bonus": f2_scores["total"],
    }
    f1_final, f2_final, conf_raw = _apply_combination_logic(event_result, natal_cmp, w)

    predicted_winner = fighter1_name if f1_final >= f2_final else fighter2_name
    confidence = max(50.0, min(99.0, round(50.0 + min(conf_raw * 2.5, 49.0), 1)))

    def planet_detail(chart, house_map):
        rows = []
        for p in chart["planets"]:
            name = p["planet"]
            sign = p["sign"]
            house = house_map.get(name, 0)
            dig = dignity_score(name, sign, w)
            hs = house_score(house, w)
            rows.append({
                "planet": name,
                "sign": sign,
                "dignity": round(dig, 1),
                "horary_house": house,
                "house_score": round(hs, 1),
                "total": round(dig + hs, 1),
            })
        return rows

    return {
        "predicted_winner": predicted_winner,
        "confidence": confidence,
        "fighter1": {
            "name": fighter1_name,
            "vitality": round(f1_scores["vitality"], 2),
            "alertness": round(f1_scores["alertness"], 2),
            "temperament": round(f1_scores["temperament"], 2),
            "total": round(f1_scores["total"], 2),
            "planets": planet_detail(f1_chart, f1_house_map),
        },
        "fighter2": {
            "name": fighter2_name,
            "vitality": round(f2_scores["vitality"], 2),
            "alertness": round(f2_scores["alertness"], 2),
            "temperament": round(f2_scores["temperament"], 2),
            "total": round(f2_scores["total"], 2),
            "planets": planet_detail(f2_chart, f2_house_map),
        },
        "horary_chart": {
            "fighter1_score": round(event_result["champion_score"], 2),
            "fighter2_score": round(event_result["challenger_score"], 2),
            "planet_assignments": event_result["planet_assignments"],
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
