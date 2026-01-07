import os
from flask import Flask, request, jsonify, render_template
from services.planner import plan_trip, plan_trip_via
from services.vehicles_gql import fetch_vehicles, fetch_vehicle_details
from services.geocoding import geocode

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/vehicles")
def api_vehicles():
    return jsonify(fetch_vehicles())

@app.route("/api/vehicle/<vehicle_id>")
def api_vehicle(vehicle_id):
    return jsonify(fetch_vehicle_details(vehicle_id))

@app.route("/api/plan", methods=["POST"])
def api_plan():
    data_json = request.json

    # Géocodage des adresses
    from_coord = geocode(data_json["from"])
    to_coord = geocode(data_json["to"])

    # Construire le dictionnaire attendu par plan_trip
    data = {
        "from_coord": from_coord,
        "to_coord": to_coord,
        "vehicle_id": data_json["vehicle_id"],
        "mode": data_json.get("mode", "normal")
    }

    result = plan_trip(data)
    return jsonify(result)

@app.route("/api/plan_via", methods=["POST"])
def api_plan_via():
    data_json = request.json

    from_coord = geocode(data_json["from"])
    to_coord = geocode(data_json["to"])
    via_coord = geocode(data_json["via"])

    data = {
        "from_coord": from_coord,
        "to_coord": to_coord,
        "via_coord": via_coord,
        "vehicle_id": data_json["vehicle_id"]
    }

    result = plan_trip_via(data)
    return jsonify(result)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
