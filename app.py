"""
Bradley Astro Boxing Oracle — Flask web application.

Accepts venue + bell time + two fighters' birthdates,
returns a prediction using the horary chart methodology.

Run:
    cd /home/user/bradley && python app.py
Then open http://localhost:5000 in your browser.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify
from backtester import analyze_fight_live

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)

        fighter1_name = data["fighter1_name"].strip()
        fighter1_birthdate = data["fighter1_birthdate"].strip()
        fighter2_name = data["fighter2_name"].strip()
        fighter2_birthdate = data["fighter2_birthdate"].strip()

        venue_lat = float(data["venue_lat"])
        venue_lon = float(data["venue_lon"])

        # Combine date + time + offset into ISO 8601
        bell_date = data["bell_date"].strip()        # "YYYY-MM-DD"
        bell_time = data["bell_time"].strip()        # "HH:MM"
        tz_offset = data["tz_offset"].strip()        # e.g. "-08:00" or "+05:30"

        if not tz_offset.startswith(("+", "-")):
            tz_offset = "+" + tz_offset
        venue_datetime = f"{bell_date}T{bell_time}:00{tz_offset}"

        result = analyze_fight_live(
            fighter1_name=fighter1_name,
            fighter1_birthdate=fighter1_birthdate,
            fighter2_name=fighter2_name,
            fighter2_birthdate=fighter2_birthdate,
            venue_datetime=venue_datetime,
            venue_lat=venue_lat,
            venue_lon=venue_lon,
        )
        return jsonify({"ok": True, "result": result})

    except Exception as exc:
        import traceback
        return jsonify({"ok": False, "error": str(exc),
                        "trace": traceback.format_exc()}), 400


@app.route("/geocode", methods=["POST"])
def geocode():
    """Forward a venue name to Nominatim and return lat/lon."""
    try:
        import requests as req
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"ok": False, "error": "empty query"}), 400

        resp = req.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1},
            headers={"User-Agent": "BradleyAstroBoxing/1.0"},
            timeout=8,
        )
        results = resp.json()
        if not results:
            return jsonify({"ok": False, "error": "No results found"}), 404

        top = results[0]
        return jsonify({
            "ok": True,
            "lat": float(top["lat"]),
            "lon": float(top["lon"]),
            "display_name": top["display_name"],
        })
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


if __name__ == "__main__":
    print("Bradley Astro Boxing Oracle")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
