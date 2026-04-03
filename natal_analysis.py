"""
Bradley's natal strength factors.

Factors:
  Vitality    — Sun, Moon, Mars
  Alertness   — Mercury, Uranus
  Temperament — Venus, Jupiter, Saturn

Each planet is scored by dignity + house placement.
"""

from dignities import dignity_score

VITALITY_PLANETS = ["Sun", "Moon", "Mars"]
ALERTNESS_PLANETS = ["Mercury", "Uranus"]
TEMPERAMENT_PLANETS = ["Venus", "Jupiter", "Saturn"]

ANGULAR_HOUSES = {1, 4, 7, 10}
SUCCEDENT_HOUSES = {2, 5, 8, 11}
CADENT_HOUSES = {3, 6, 9, 12}

DEFAULT_WEIGHTS = {
    "domicile": 5,
    "exaltation": 4,
    "detriment": -5,
    "fall": -4,
    "neutral": 0,
    "angular": 3,
    "succedent": 1,
    "cadent": -1,
    "vitality_w": 1.0,
    "alertness_w": 1.0,
    "temperament_w": 1.0,
}


def house_score(house: int, weights: dict) -> float:
    """Return angular/succedent/cadent score for a house number."""
    if house in ANGULAR_HOUSES:
        return float(weights.get("angular", 3))
    if house in SUCCEDENT_HOUSES:
        return float(weights.get("succedent", 1))
    return float(weights.get("cadent", -1))


def _planet_score(planet_data: dict, weights: dict) -> float:
    """Total score for one planet: dignity + house."""
    d = dignity_score(planet_data["planet"], planet_data["sign"], weights)
    h = house_score(planet_data["house"], weights)
    return d + h


def score_factor(planets_data: list, planet_names: list, weights: dict) -> float:
    """
    Sum scores for the subset of planets in planet_names.

    Args:
        planets_data: list of planet dicts from chart["planets"]
        planet_names: list of planet names to include
        weights: combined dignity + house weights dict
    """
    lookup = {p["planet"]: p for p in planets_data}
    total = 0.0
    for name in planet_names:
        if name in lookup:
            total += _planet_score(lookup[name], weights)
    return total


def analyze_natal_chart(chart: dict, weights: dict = None) -> dict:
    """
    Compute Bradley's three natal strength factors for a chart.

    Returns:
        {
          "vitality": float,
          "alertness": float,
          "temperament": float,
          "total": float
        }
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    planets = chart["planets"]
    v = score_factor(planets, VITALITY_PLANETS, w) * w.get("vitality_w", 1.0)
    a = score_factor(planets, ALERTNESS_PLANETS, w) * w.get("alertness_w", 1.0)
    t = score_factor(planets, TEMPERAMENT_PLANETS, w) * w.get("temperament_w", 1.0)
    return {
        "vitality": v,
        "alertness": a,
        "temperament": t,
        "total": v + a + t,
    }


def compare_natal_fighters(champ_chart: dict, chall_chart: dict,
                            weights: dict = None) -> dict:
    """
    Compare natal strength factors between champion and challenger.

    Returns:
        {
          "champion_vitality": float, "challenger_vitality": float,
          "vitality_dominant": "champion"|"challenger"|"even",
          "champion_alertness": float, "challenger_alertness": float,
          "alertness_dominant": str,
          "champion_temperament": float, "challenger_temperament": float,
          "temperament_dominant": str,
          "champion_bonus": float,  # weighted total
          "challenger_bonus": float,
        }
    """
    champ = analyze_natal_chart(champ_chart, weights)
    chall = analyze_natal_chart(chall_chart, weights)

    def dominant(cv, xv):
        if cv > xv:
            return "champion"
        elif xv > cv:
            return "challenger"
        return "even"

    return {
        "champion_vitality": champ["vitality"],
        "challenger_vitality": chall["vitality"],
        "vitality_dominant": dominant(champ["vitality"], chall["vitality"]),
        "champion_alertness": champ["alertness"],
        "challenger_alertness": chall["alertness"],
        "alertness_dominant": dominant(champ["alertness"], chall["alertness"]),
        "champion_temperament": champ["temperament"],
        "challenger_temperament": chall["temperament"],
        "temperament_dominant": dominant(champ["temperament"], chall["temperament"]),
        "champion_bonus": champ["total"],
        "challenger_bonus": chall["total"],
    }
