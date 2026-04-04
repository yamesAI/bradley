"""
Load fights from the OpenBoxing API (https://openboxing.org/api/bouts/all.json)
and transform them into the fight dict format used by the backtester.

API facts:
- 6,986 total bouts, 1912–2023, all weight classes
- Fighter name: either {first, last, short} object or plain string
- Fighter born: "YYYY-MM-DD" when available (only for fighters with championId)
- Location: effectively always null (0.014% non-null) → use hardcoded defaults
- Result winner: "BOXER A", "BOXER B", or "DRAW"

Limitations:
- Birth times unknown → use noon UTC (12:00:00Z)
- Fight times unknown → use 22:00:00Z
- Fight location unknown → use NYC coordinates
- Birth locations: hardcoded for known champions, default for the rest
"""

import requests

API_URL = "https://openboxing.org/api/bouts/all.json"
REQUEST_TIMEOUT = 30

FIGHT_DEFAULT_TIME = "T22:00:00Z"
BIRTH_DEFAULT_TIME = "T12:00:00Z"
DEFAULT_FIGHT_LOCATION = (40.7128, -74.0060)   # New York City
DEFAULT_BIRTH_LOCATION = (40.0, -75.0)          # mid-Atlantic US (unknown)

# Known birth locations for champions who appear in the API.
# Name format: "First Last" matching parse_name() output.
BOXER_BIRTHPLACES = {
    # Heavyweight
    "Jack Johnson":       (29.3,  -94.8),   # Galveston, TX
    "Jess Willard":       (39.1,  -96.6),   # St. Clere, KS
    "Jack Dempsey":       (37.2, -105.9),   # Manassa, CO
    "Gene Tunney":        (40.7,  -74.0),   # New York City
    "Max Schmeling":      (53.8,   10.0),   # Klein Luckow, Germany
    "Primo Carnera":      (46.2,   12.8),   # Sequals, Italy
    "Max Baer":           (41.2,  -96.0),   # Omaha, NE
    "James Braddock":     (40.7,  -74.0),   # New York City area
    "Joe Louis":          (33.7,  -85.0),   # Lafayette, AL
    "Ezzard Charles":     (33.5,  -82.0),   # Lawrenceville, GA
    "Jersey Joe Walcott": (39.9,  -75.1),   # Merchantville, NJ
    "Rocky Marciano":     (42.1,  -71.0),   # Brockton, MA
    "Floyd Patterson":    (35.4,  -80.6),   # Waco, NC
    "Ingemar Johansson":  (57.7,   12.0),   # Gothenburg, Sweden
    "Sonny Liston":       (35.0,  -90.8),   # Forrest City, AR
    "Muhammad Ali":       (38.2,  -85.7),   # Louisville, KY
    "Cassius Clay":       (38.2,  -85.7),   # Louisville, KY
    "Joe Frazier":        (32.4,  -80.7),   # Beaufort, SC
    "George Foreman":     (32.5,  -94.4),   # Marshall, TX
    "Ken Norton":         (39.7,  -90.2),   # Jacksonville, IL
    "Larry Holmes":       (31.8,  -84.8),   # Cuthbert, GA
    "Mike Tyson":         (40.7,  -73.9),   # Brooklyn, NY
    "Evander Holyfield":  (31.0,  -87.5),   # Atmore, AL
    "Lennox Lewis":       (51.5,    0.0),   # West Ham, London
    # Light Heavyweight / Middleweight / others common in early API data
    "Georges Carpentier": (50.4,    2.8),   # Liévin, France
    "Frank Klaus":        (40.4,  -79.9),   # Pittsburgh, PA
    "Eugene Criqui":      (48.8,    2.3),   # Paris, France
    "Jimmy Wilde":        (51.6,   -3.3),   # Merthyr, Wales
    "Benny Leonard":      (40.7,  -74.0),   # New York City
    "Freddie Welsh":      (51.6,   -3.3),   # Pontypridd, Wales
    "Pete Herman":        (29.9,  -90.1),   # New Orleans, LA
    "Kid Williams":       (55.7,   12.6),   # Copenhagen, Denmark
    "Joe Symonds":        (51.5,   -0.1),   # London, England
    "Al McCoy":           (40.7,  -74.0),   # New York
    "Sid Smith":          (51.5,   -0.1),   # London
    "Bob Moha":           (46.9,  -91.9),   # Duluth, MN
    "Johnny Kilbane":     (41.5,  -81.7),   # Cleveland, OH
    "Johnny Dundee":      (38.1,   13.4),   # Palermo, Sicily
    "Abe Attell":         (37.8, -122.4),   # San Francisco, CA
    "Willie Ritchie":     (37.8, -122.4),   # San Francisco, CA
    "Ad Wolgast":         (43.8,  -86.4),   # Cadillac, MI
    "Battling Nelson":    (55.7,   12.6),   # Copenhagen, Denmark
    "Mickey Walker":      (40.2,  -74.0),   # Elizabeth, NJ
    "Tiger Flowers":      (33.8,  -85.2),   # Camille, GA
    "Harry Greb":         (40.4,  -79.9),   # Pittsburgh, PA
    "Tommy Loughran":     (40.0,  -75.1),   # Philadelphia, PA
    "Maxie Rosenbloom":   (40.7,  -74.0),   # New York City
    "Bob Fitzsimmons":    (50.1,   -5.5),   # Helston, England
    "Jim Jeffries":       (34.1, -118.2),   # Burrell Township, OH (raised CA)
    "Tommy Burns":        (43.5,  -80.5),   # Hanover, Canada
    "Jack Sharkey":       (42.4,  -71.1),   # Binghamton, NY
    "Primo Carnera":      (46.2,   12.8),   # Sequals, Italy
    "Lou Brouillard":     (45.5,  -73.6),   # Montreal, Canada
    "Young Corbett":      (40.7,  -74.0),   # New York
    "Ted Kid Lewis":      (51.5,   -0.1),   # London
    "Jack Britton":       (42.9,  -78.9),   # Clinton, NY
    "Harry Lewis":        (40.7,  -74.0),   # New York
    "Charley White":      (51.5,   -0.1),   # Liverpool, England
    "Lew Tendler":        (40.0,  -75.1),   # Philadelphia, PA
    "Rocky Kansas":       (42.9,  -78.9),   # Buffalo, NY
    "Pancho Villa":       (14.6,  121.1),   # Iloilo, Philippines
    "Pete Latzo":         (41.4,  -75.7),   # Colerain, PA
    "Joe Dundee":         (38.1,   13.4),   # Palermo, Sicily
}


def fetch_bouts() -> list:
    """Fetch all bouts from the OpenBoxing API. Returns raw JSON list."""
    resp = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def parse_name(name_field) -> str | None:
    """
    Handle both fighter name formats:
      dict  {first, last, short} → "First Last"
      str   "Plain String"       → "Plain String"
      None/missing               → None
    """
    if name_field is None:
        return None
    if isinstance(name_field, dict):
        first = name_field.get("first", "")
        last = name_field.get("last", "")
        if first and last:
            return f"{first} {last}"
        # Fallback to 'short' if first/last are missing
        return name_field.get("short") or None
    if isinstance(name_field, str):
        return name_field.strip() or None
    return None


def parse_born(boxer: dict) -> str | None:
    """Return YYYY-MM-DD birth date string, or None if unavailable."""
    born = boxer.get("born")
    if isinstance(born, str) and len(born) == 10:
        return born
    return None


def get_birth_location(name: str) -> tuple:
    """Return known birth coordinates or DEFAULT_BIRTH_LOCATION."""
    return BOXER_BIRTHPLACES.get(name, DEFAULT_BIRTH_LOCATION)


def transform_bout(bout: dict) -> dict | None:
    """
    Convert an API bout record into a backtester fight dict.

    Returns None when:
      - Either fighter is missing a born date
      - Result winner is "DRAW"
      - Status is not "FINISHED"

    Convention: boxerA = champion, boxerB = challenger.
    """
    if bout.get("status") != "FINISHED":
        return None

    result = bout.get("result", {})
    winner_str = (result.get("winner") or "").upper()
    if winner_str == "DRAW":
        return None

    boxers = bout.get("boxers", {})
    boxer_a = boxers.get("boxerA", {})
    boxer_b = boxers.get("boxerB", {})

    name_a = parse_name(boxer_a.get("name"))
    name_b = parse_name(boxer_b.get("name"))
    born_a = parse_born(boxer_a)
    born_b = parse_born(boxer_b)

    # Both fighters must have names and birth dates
    if not name_a or not name_b or not born_a or not born_b:
        return None

    date_str = bout.get("date", "")
    if not date_str or len(date_str) < 10:
        return None

    # Determine winner name
    if winner_str == "BOXER A":
        actual_winner = name_a
    elif winner_str == "BOXER B":
        actual_winner = name_b
    else:
        return None  # Unexpected winner string

    weight_obj = bout.get("weight", {})
    weight_class = weight_obj.get("class", "Unknown")

    return {
        "fight": f"{name_a} vs {name_b}",
        "datetime": date_str + FIGHT_DEFAULT_TIME,
        "location": DEFAULT_FIGHT_LOCATION,
        "weight_class": weight_class,
        "champion": {
            "name": name_a,
            "birth_datetime": born_a + BIRTH_DEFAULT_TIME,
            "birth_location": get_birth_location(name_a),
        },
        "challenger": {
            "name": name_b,
            "birth_datetime": born_b + BIRTH_DEFAULT_TIME,
            "birth_location": get_birth_location(name_b),
        },
        "actual_winner": actual_winner,
        "method": result.get("methodOfVictory", ""),
        "round": result.get("totalRounds"),
    }


def load_api_fights(n: int = 100) -> list:
    """
    Fetch all bouts from the API, filter to valid fights (both fighters have
    birth dates, no draws, finished), and return the first n.

    Prints a summary of how many bouts were fetched vs. valid.
    """
    print(f"Fetching bouts from {API_URL} ...")
    bouts = fetch_bouts()
    print(f"  Fetched {len(bouts)} total bouts")

    fights = []
    skipped_no_born = 0
    skipped_draw = 0
    skipped_other = 0

    for bout in bouts:
        if len(fights) >= n:
            break

        result = bout.get("result", {})
        winner_str = (result.get("winner") or "").upper()

        # Track skip reasons for reporting
        boxers = bout.get("boxers", {})
        boxer_a = boxers.get("boxerA", {})
        boxer_b = boxers.get("boxerB", {})
        born_a = parse_born(boxer_a)
        born_b = parse_born(boxer_b)

        if winner_str == "DRAW":
            skipped_draw += 1
            continue
        if not born_a or not born_b:
            skipped_no_born += 1
            continue

        fight = transform_bout(bout)
        if fight is None:
            skipped_other += 1
            continue

        fights.append(fight)

    print(f"  Valid fights found: {len(fights) + skipped_draw + skipped_other + len(fights)}")
    print(f"  Skipped — missing birth date: {skipped_no_born}")
    print(f"  Skipped — draw result:        {skipped_draw}")
    print(f"  Skipped — other:              {skipped_other}")
    print(f"  Using first {len(fights)} fights for backtest\n")

    return fights
