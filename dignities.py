"""
Classical essential dignity tables for the nine planets.
Provides domicile, exaltation, detriment, and fall lookups.
"""

# Traditional (pre-modern) domicile rulerships
# Uranus/Neptune get modern rulerships as secondary entries
DOMICILE = {
    "Sun":     ["Leo"],
    "Moon":    ["Cancer"],
    "Mercury": ["Gemini", "Virgo"],
    "Venus":   ["Taurus", "Libra"],
    "Mars":    ["Aries", "Scorpio"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Saturn":  ["Capricorn", "Aquarius"],
    "Uranus":  ["Aquarius"],
    "Neptune": ["Pisces"],
}

EXALTATION = {
    "Sun":     "Aries",
    "Moon":    "Taurus",
    "Mercury": "Virgo",
    "Venus":   "Pisces",
    "Mars":    "Capricorn",
    "Jupiter": "Cancer",
    "Saturn":  "Libra",
    "Uranus":  "Scorpio",
    "Neptune": "Leo",
}

# Detriment = opposite of domicile sign(s)
_OPPOSITE = {
    "Aries": "Libra", "Taurus": "Scorpio", "Gemini": "Sagittarius",
    "Cancer": "Capricorn", "Leo": "Aquarius", "Virgo": "Pisces",
    "Libra": "Aries", "Scorpio": "Taurus", "Sagittarius": "Gemini",
    "Capricorn": "Cancer", "Aquarius": "Leo", "Pisces": "Virgo",
}

DETRIMENT = {
    planet: [_OPPOSITE[s] for s in signs]
    for planet, signs in DOMICILE.items()
}

# Fall = opposite of exaltation sign
FALL = {
    planet: _OPPOSITE[sign]
    for planet, sign in EXALTATION.items()
}

# Default dignity score values (tunable)
DEFAULT_DIGNITY_SCORES = {
    "domicile":  5,
    "exaltation": 4,
    "detriment": -5,
    "fall":      -4,
    "neutral":    0,
}


def dignity_score(planet: str, sign: str, scores: dict = None) -> float:
    """
    Return the essential dignity score for a planet in a given sign.

    Args:
        planet: planet name e.g. "Sun"
        sign: zodiac sign name e.g. "Taurus"
        scores: dict with keys domicile/exaltation/detriment/fall/neutral

    Returns:
        float score
    """
    if scores is None:
        scores = DEFAULT_DIGNITY_SCORES

    if sign in DOMICILE.get(planet, []):
        return float(scores["domicile"])
    if sign == EXALTATION.get(planet):
        return float(scores["exaltation"])
    if sign in DETRIMENT.get(planet, []):
        return float(scores["detriment"])
    if sign == FALL.get(planet):
        return float(scores["fall"])
    return float(scores.get("neutral", 0))
