from flask import Flask, request, jsonify
from bahire_hasab import get_bahire_hasab, to_gc
from constants import HOLIDAY_INFO, FIXED_HOLIDAYS

app = Flask(__name__)

@app.route("/")
def home():
    return "Ethiopian Calendar & Bahire Hasab API is running"

@app.route("/bahire-hasab", methods=["GET"])
def bahire_hasab_api():
    year = request.args.get("year")

    if not year or not year.isdigit():
        return jsonify({"error": "Please provide a valid Ethiopian year"}), 400

    year = int(year)
    bh = get_bahire_hasab(year)

    result = {
        "year": year,
        "metqi": bh["metqi"],
        "bealeMetqi": bh["bealeMetqi"],
        "nineveh": bh["nineveh"],
        "movableFeasts": bh["movableFeasts"],
        "fixedHolidays": []
    }

    for key, info in FIXED_HOLIDAYS.items():
        holiday_info = HOLIDAY_INFO.get(key, {})
        gc = to_gc(year, info["month"], info["day"])

        result["fixedHolidays"].append({
            "key": key,
            "ethiopian": {
                "year": year,
                "month": info["month"],
                "day": info["day"]
            },
            "gregorian": {
                "year": gc.year,
                "month": gc.month,
                "day": gc.day
            },
            "name": holiday_info.get("name", {}),
            "description": holiday_info.get("description", {})
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
