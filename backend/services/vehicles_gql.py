import os
import requests

GQL_URL = "https://api.chargetrip.io/graphql"

# Clé publique Chargetrip (accès limité mais suffisante pour tests)
CLIENT_ID = "693a928471c4b62cdd1c4e2c"
APP_ID = "693a928471c4b62cdd1c4e2e"

def fetch_vehicles():
    query = """
    query vehicleList {
      vehicleList(page: 0, size: 20) {
        id
        naming {
          make
          model
          chargetrip_version
        }
        media {
          image {
            thumbnail_url
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "x-client-id": "693a928471c4b62cdd1c4e2c",
        "x-app-id": "693a928471c4b62cdd1c4e2e"
    }

    response = requests.post(GQL_URL, json={"query": query}, headers=headers)

    try:
        response.raise_for_status()
    except Exception:
        raise Exception(f"Erreur API Chargetrip : {response.text}")

    data = response.json().get("data", {}).get("vehicleList", [])

    vehicles = []
    for v in data:
        vehicles.append({
            "id": v["id"],
            "make": v["naming"]["make"],
            "model": v["naming"]["model"],
            "version": v["naming"]["chargetrip_version"],
            "thumbnail": v["media"]["image"]["thumbnail_url"]
        })

    return vehicles

def fetch_vehicle_details(vehicle_id):
    query = """
    query vehicle($vehicleId: ID!) {
      vehicle(id: $vehicleId) {
        naming {
          make
          model
          chargetrip_version
        }
        media {
          image {
            url
            thumbnail_url
          }
          brand {
            thumbnail_url
          }
        }
        battery {
          usable_kwh
        }
        range {
          best {
            highway
            city
            combined
          }
          worst {
            highway
            city
            combined
          }
          chargetrip_range {
            best
            worst
          }
        }
        routing {
          fast_charging_support
        }
        connectors {
          standard
        }
        performance {
          acceleration
          top_speed
        }
      }
    }
    """

    variables = { "vehicleId": vehicle_id }

    headers = {
        "Content-Type": "application/json",
        "x-client-id": CLIENT_ID,
        "x-app-id": APP_ID
    }

    response = requests.post(
        GQL_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )

    response.raise_for_status()

    data = response.json().get("data", {}).get("vehicle")

    if data is None:
        raise Exception(f"Aucun véhicule trouvé pour l'id {vehicle_id}")

    return data
