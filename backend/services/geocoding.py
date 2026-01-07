import requests

def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    r = requests.get(
        url,
        params=params,
        headers={"User-Agent": "evtrip"}
    ).json()

    if not r:
        raise ValueError("Adresse introuvable")

    return float(r[0]["lat"]), float(r[0]["lon"])
