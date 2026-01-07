import os
from flask import Flask, request, jsonify, render_template
from services.planner import plan_trip
from services.vehicles_gql import fetch_vehicles
from services.charger_client import nearby_chargers
from services.routing_client import route_between

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/vehicle/<vehicle_id>', methods=['GET'])
def api_vehicle_details(vehicle_id):
    from services.vehicles_gql import fetch_vehicle_details
    details = fetch_vehicle_details(vehicle_id)
    return jsonify(details)



@app.route('/api/plan', methods=['POST'])
def api_plan():
    data = request.json
    plan = plan_trip(data)
    return jsonify(plan)


@app.route('/api/vehicles', methods=['GET'])
def api_vehicles():
    vehicles = fetch_vehicles()
    return jsonify(vehicles)


@app.route('/api/chargers', methods=['GET'])
def api_chargers():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    res = nearby_chargers(float(lat), float(lon))
    return jsonify(res)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
