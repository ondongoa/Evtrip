import requests
from math import radians, sin, cos, sqrt, atan2

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjZlMWI2ZjBhZDkxYjRmZTE4NDU3ZDE4Y2Y4MWQ1NjBhIiwiaCI6Im11cm11cjY0In0="

def route_between(p1, p2):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [p1[1], p1[0]],
            [p2[1], p2[0]]
        ]
    }

    r = requests.post(url, json=body, headers=headers)
    r.raise_for_status()

    j = r.json()
    coords = j["features"][0]["geometry"]["coordinates"]
    coords_latlon = [(c[1], c[0]) for c in coords]

    distance_km = j["features"][0]["properties"]["summary"]["distance"] / 1000

    return {
        "coords": coords_latlon,
        "distance_km": distance_km
    }

def distance_between_points(p1, p2):
    R = 6371
    lat1, lon1 = p1
    lat2, lon2 = p2

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))
