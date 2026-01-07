from math import ceil
from services.routing_client import route_between, distance_between_points
from services.charger_client import nearby_chargers
from services.vehicles_gql import fetch_vehicle_details

DRIVING_MODES = {
    "eco": 0.9,
    "normal": 0.8,
    "fast": 0.7,
    "safe": 0.6
}


def cumulative_distances(coords):
    dists = [0.0]
    total = 0.0
    for i in range(1, len(coords)):
        total += distance_between_points(coords[i - 1], coords[i])
        dists.append(total)
    return dists


def find_point_at_distance(coords, cum_dists, target_km):
    for i, d in enumerate(cum_dists):
        if d >= target_km:
            return coords[i]
    return coords[-1]


def choose_best_charger(chargers, ref_point):
    best = None
    best_score = -1e9

    for c in chargers:
        power = c.get("power_kW") or 11
        dist = distance_between_points(ref_point, (c["lat"], c["lon"]))
        score = (power * 2) - dist

        if score > best_score:
            best_score = score
            best = c

    return best


def plan_trip(data):
    vehicle = fetch_vehicle_details(data["vehicle_id"])

    autonomy = (
        vehicle["range"]
        .get("chargetrip_range", {})
        .get("best")
        or vehicle["range"]["best"]["combined"]
    )

    if not autonomy:
        raise ValueError("Autonomie introuvable")

    mode = data.get("mode", "normal")
    factor = DRIVING_MODES.get(mode, 0.8)

    usable_range = autonomy * factor
    usable_range = max(120, min(usable_range, 180))

    route = route_between(
        tuple(data["from_coord"]),
        tuple(data["to_coord"])
    )

    base_coords = route["coords"]
    total_distance = route["distance_km"]

    if total_distance <= usable_range:
        nb_stops = 0
    else:
        nb_stops = ceil(total_distance / usable_range) - 1

    nb_stops = max(1, min(nb_stops, 10))

    cum_dists = cumulative_distances(base_coords)
    segment_km = total_distance / (nb_stops + 1)

    stops = []

    for i in range(1, nb_stops + 1):
        point = find_point_at_distance(
            base_coords,
            cum_dists,
            segment_km * i
        )

        chargers = nearby_chargers(
            point[0],
            point[1],
            radius=50,
            rows=6
        )

        if chargers:
            best = choose_best_charger(chargers, point)
            if best:
                stops.append({
                    "lat": best["lat"],
                    "lon": best["lon"],
                    "name": best["name"],
                    "power_kW": best.get("power_kW"),
                    "expected_charge_min": 30
                })

    # 🔁 recalcul du trajet réel via bornes
    full_coords = []
    current = tuple(data["from_coord"])

    for stop in stops:
        r = route_between(current, (stop["lat"], stop["lon"]))
        full_coords += r["coords"]
        current = (stop["lat"], stop["lon"])

    r = route_between(current, tuple(data["to_coord"]))
    full_coords += r["coords"]

    drive_time_h = total_distance / 90
    charge_time_h = len(stops) * 0.5

    return {
        "distance_km": round(total_distance, 1),
        "nb_stops": len(stops),
        "mode": mode,
        "drive_time_h": round(drive_time_h, 2),
        "charge_time_h": round(charge_time_h, 2),
        "total_time_h": round(drive_time_h + charge_time_h, 2),
        "stops": stops,
        "coords": full_coords
    }


def plan_trip_via(data):
    route1 = route_between(
        tuple(data["from_coord"]),
        tuple(data["via_coord"])
    )

    route2 = route_between(
        tuple(data["via_coord"]),
        tuple(data["to_coord"])
    )

    coords = route1["coords"] + route2["coords"][1:]
    total_distance = route1["distance_km"] + route2["distance_km"]

    return {
        "distance_km": round(total_distance, 1),
        "coords": coords,
        "stops": [{
            "lat": data["via_coord"][0],
            "lon": data["via_coord"][1],
            "name": "Borne sélectionnée",
            "expected_charge_min": 30
        }]
    }
