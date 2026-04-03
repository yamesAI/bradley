"""
Event chart analysis for the fight datetime and location.

Horary tradition: houses 1-6 belong to the champion (querent/defender),
houses 7-12 belong to the challenger (opponent).

Planets in each half are scored and summed to give each side an event score.
"""

from ephemeris import get_chart_dict
from natal_analysis import _planet_score

CHAMPION_HOUSES = {1, 2, 3, 4, 5, 6}
CHALLENGER_HOUSES = {7, 8, 9, 10, 11, 12}


def analyze_event_chart(fight_datetime: str, lat: float, lon: float,
                        weights: dict = None) -> dict:
    """
    Compute event chart scores for champion and challenger sides.

    Args:
        fight_datetime: UTC ISO 8601 string of the fight start time
        lat: fight venue latitude
        lon: fight venue longitude
        weights: dignity + house weights dict

    Returns:
        {
          "champion_score": float,
          "challenger_score": float,
          "dominant": "champion"|"challenger"|"even",
          "planet_assignments": [{"planet": str, "house": int, "side": str, "score": float}]
        }
    """
    w = weights or {}
    chart = get_chart_dict(fight_datetime, lat, lon)

    champion_score = 0.0
    challenger_score = 0.0
    assignments = []

    for p in chart["planets"]:
        score = _planet_score(p, w)
        house = p["house"]
        if house in CHAMPION_HOUSES:
            champion_score += score
            side = "champion"
        else:
            challenger_score += score
            side = "challenger"
        assignments.append({
            "planet": p["planet"],
            "house": house,
            "side": side,
            "score": round(score, 3),
        })

    if champion_score > challenger_score:
        dominant = "champion"
    elif challenger_score > champion_score:
        dominant = "challenger"
    else:
        dominant = "even"

    return {
        "champion_score": round(champion_score, 4),
        "challenger_score": round(challenger_score, 4),
        "dominant": dominant,
        "planet_assignments": assignments,
    }
