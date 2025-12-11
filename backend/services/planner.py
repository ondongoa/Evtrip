from .routing_client import route_between, distance_between_points
from .charger_client import nearby_chargers
from .vehicles_gql import fetch_vehicle_details


def compute_stops(route_coords, vehicle):
    """
    Calcule les arrêts de recharge nécessaires selon l'autonomie réelle du véhicule.
    """
    autonomy = vehicle["range"]["chargetrip_range"]["best"]
    battery_kwh = vehicle["battery"]["usable_kwh"]
    
    stops = []
    distance_since_charge = 0.0
    last_point = route_coords[0]

    for point in route_coords[1:]:
        d = distance_between_points(last_point, point)
        distance_since_charge += d
        last_point = point

        # Si on approche de 90% de l'autonomie
        if distance_since_charge >= autonomy * 0.9:
            candidates = nearby_chargers(point[0], point[1])
            if candidates:
                stop = candidates[0]
                # Estimation du temps de charge (basique : 30 min)
                expected_time_min = 30  
                stops.append({
                    'lat': stop['lat'],
                    'lon': stop['lon'],
                    'name': stop.get('name'),
                    'expected_charge_min': expected_time_min
                })
                distance_since_charge = 0.0

    return stops


def plan_trip(data):
    """
    Planifie un trajet avec les arrêts de recharge et temps estimé.
    """
    # Récupérer les détails réels du véhicule
    vehicle_id = data.get('vehicle_id')
    vehicle = fetch_vehicle_details(vehicle_id)

    # Récupérer l'itinéraire
    route = route_between(
        tuple(data['from_coord']),
        tuple(data['to_coord'])
    )

    coords = route['coords']
    distance_km = route['distance_km']

    # Calcul des arrêts
    stops = compute_stops(coords, vehicle)

    # Calcul du temps
    avg_speed_kmh = 90  # vitesse moyenne
    drive_time_h = distance_km / avg_speed_kmh
    charge_time_h = sum(s['expected_charge_min'] for s in stops) / 60.0
    total_time_h = drive_time_h + charge_time_h

    return {
        'distance_km': distance_km,
        'drive_time_h': drive_time_h,
        'charge_time_h': charge_time_h,
        'total_time_h': total_time_h,
        'stops': stops,
        'coords': coords
    }
