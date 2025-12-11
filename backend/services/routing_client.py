import os
import requests
from math import radians, sin, cos, sqrt, atan2

ORS_API_KEY = os.environ.get("ORS_API_KEY")


def route_between(from_coord, to_coord):
    # from_coord = (lat, lon)
    # to_coord = (lat, lon)

    # Mode fallback si pas de clé ORS
    if not ORS_API_KEY:
        coords = [from_coord, to_coord]
        distance_km = distance_between_points(from_coord, to_coord)
        return {
            "distance_km": distance_km,
            "coords": coords
        }

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [from_coord[1], from_coord[0]],
            [to_coord[1], to_coord[0]]
        ]
    }

    r = requests.post(url, json=body, headers=headers, timeout=10)
    r.raise_for_status()

    j = r.json()
    summary = j["features"][0]["properties"]["summary"]
    distance_km = summary["distance"] / 1000.0

    coords = j["features"][0]["geometry"]["coordinates"]
    coords_latlon = [(c[1], c[0]) for c in coords]

    return {
        "distance_km": distance_km,
        "coords": coords_latlon
    }


def distance_between_points(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2

    R = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (sin(dlat / 2) ** 2 +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon / 2) ** 2)

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
