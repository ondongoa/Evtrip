import requests

API_KEY = "cd3f04e4-2dcf-4878-a944-85f8ad9e6ca0"  # facultatif pour tests
BASE = "https://api.openchargemap.io/v3/poi/"

def nearby_chargers(lat, lon, radius=50, rows=10):
    params = {
        "output": "json",
        "latitude": lat,
        "longitude": lon,
        "distance": radius,   # en km
        "distanceunit": "KM",
        "maxresults": rows,
        "compact": True,
        "verbose": False
    }

    headers = {
        "User-Agent": "evtrip"
    }

    if API_KEY:
        headers["X-API-Key"] = API_KEY

    r = requests.get(BASE, params=params, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()
    results = []

    for c in data:
        addr = c.get("AddressInfo", {})
        lat_c = addr.get("Latitude")
        lon_c = addr.get("Longitude")

        if lat_c is None or lon_c is None:
            continue

        connections = c.get("Connections") or []
        power = None

        if len(connections) > 0:
            power = connections[0].get("PowerKW")

        results.append({
            "name": addr.get("Title", "Borne"),
            "lat": lat_c,
            "lon": lon_c,
            "power_kW": power,
            "operator": c.get("OperatorInfo", {}).get("Title")
        })

    return results
