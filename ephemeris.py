"""
Swiss Ephemeris wrapper for computing natal and event charts.
Uses pyswisseph (swe) directly — no external server required.
Results are memoized to avoid redundant computation during tuning.
"""

import functools
import swisseph as swe

PLANET_CONSTS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _parse_jd(dt_utc_str: str) -> float:
    """Parse ISO 8601 UTC string to Julian Day Number."""
    s = dt_utc_str.replace("Z", "+00:00")
    # Parse manually to avoid datetime import issues with old Python
    # Format: YYYY-MM-DDTHH:MM:SS+00:00
    date_part, time_part = s.split("T")
    year, month, day = map(int, date_part.split("-"))
    # Strip timezone offset — all inputs are UTC
    time_clean = time_part.split("+")[0].split("-")[0] if "+" in time_part or (
        "-" in time_part and time_part.index("-") > 2
    ) else time_part
    # Handle the case like "00:35:00"
    h, m, sec = time_clean.split(":")
    hour_decimal = int(h) + int(m) / 60.0 + float(sec) / 3600.0
    return swe.julday(year, month, day, hour_decimal)


@functools.lru_cache(maxsize=512)
def get_chart(dt_utc_str: str, lat: float, lon: float) -> tuple:
    """
    Compute a chart for the given UTC datetime and geographic location.

    Returns a tuple (planets_tuple, asc, mc) where planets_tuple is a tuple of
    dicts (as tuples for hashability). Call _unpack_chart() to get a usable dict.

    Args:
        dt_utc_str: ISO 8601 UTC string, e.g. "1914-05-13T19:00:00Z"
        lat: geographic latitude (north positive)
        lon: geographic longitude (east positive)

    Returns:
        Packed tuple for caching. Use get_chart_dict() for a normal dict.
    """
    jd = _parse_jd(dt_utc_str)

    # Compute obliquity of ecliptic
    eps_result = swe.calc_ut(jd, swe.ECL_NUT, 0)
    eps = eps_result[0][0]

    # Compute house cusps (Placidus system)
    houses, ascmc = swe.houses(jd, lat, lon, b"P")
    asc = ascmc[0]
    mc = ascmc[1]
    armc = ascmc[2]

    planets = []
    for name, const in PLANET_CONSTS.items():
        result = swe.calc_ut(jd, const, swe.FLG_SWIEPH)
        plon = result[0][0]
        plat = result[0][1]
        sign_num = int(plon / 30) % 12
        sign = SIGNS[sign_num]
        try:
            house = int(swe.house_pos(armc, lat, eps, (plon, plat), b"P"))
        except Exception:
            house = _fallback_house(plon, houses)
        # Pack as tuple for lru_cache compatibility
        planets.append((name, sign, sign_num, round(plon, 4), house))

    return (tuple(planets), round(asc, 4), round(mc, 4))


def get_chart_dict(dt_utc_str: str, lat: float, lon: float) -> dict:
    """
    Returns a normal dict chart suitable for analysis functions.

    {
      "planets": [
        {"planet": "Sun", "sign": "Taurus", "sign_num": 1,
         "longitude": 52.2, "house": 9},
        ...
      ],
      "asc": 100.9,
      "mc": 355.1
    }
    """
    packed_planets, asc, mc = get_chart(dt_utc_str, lat, lon)
    planets = [
        {
            "planet": p[0],
            "sign": p[1],
            "sign_num": p[2],
            "longitude": p[3],
            "house": p[4],
        }
        for p in packed_planets
    ]
    return {"planets": planets, "asc": asc, "mc": mc}


def _fallback_house(planet_lon: float, houses: tuple) -> int:
    """Fallback house calculation when swe.house_pos fails."""
    lon = planet_lon % 360
    for i in range(12):
        cusp = houses[i] % 360
        next_cusp = houses[(i + 1) % 12] % 360
        if next_cusp > cusp:
            if cusp <= lon < next_cusp:
                return i + 1
        else:
            # Wrap-around (e.g. 350° to 10°)
            if lon >= cusp or lon < next_cusp:
                return i + 1
    return 1
