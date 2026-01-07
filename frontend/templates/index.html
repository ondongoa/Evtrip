let map;
let routeLayer;
let chargerMarkers = [];
let vehicleSelector;

function initMap() {
    map = L.map("map").setView([46.5, 3], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19
    }).addTo(map);
}

function clearChargers() {
    chargerMarkers.forEach(m => map.removeLayer(m));
    chargerMarkers = [];
}

function drawRoute(coords) {
    if (routeLayer) map.removeLayer(routeLayer);

    routeLayer = L.polyline(coords, {
        color: "#2563eb",
        weight: 5
    }).addTo(map);

    map.fitBounds(routeLayer.getBounds());
}

function showChargers(stops) {
    clearChargers();

    stops.forEach(stop => {
        const marker = L.marker([stop.lat, stop.lon]).addTo(map);

        marker.bindPopup(`
            <b>${stop.name}</b><br>
            Puissance : ${stop.power_kW || "?"} kW<br>
            Recharge estimée : ${stop.expected_charge_min} min<br>
            <button onclick="addVia(${stop.lat}, ${stop.lon})" class="mt-2 px-3 py-1 bg-blue-600 text-white rounded">
                Ajouter au trajet
            </button>
        `);

        chargerMarkers.push(marker);
    });
}

async function addVia(lat, lon) {
    const body = {
        from: document.getElementById("from").value,
        to: document.getElementById("to").value,
        via: [lat, lon],
        vehicle_id: vehicleSelector.value
    };

    const res = await fetch("/api/plan_via", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });

    const data = await res.json();
    drawRoute(data.coords);
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();

    vehicleSelector = document.getElementById("vehicle");

    // 🔹 Ajouter écouteur changement véhicule
    vehicleSelector.addEventListener("change", (e) => {
        loadVehicleDetails(e.target.value);
    });

    // Charger la liste des véhicules
    fetch("/api/vehicles")
        .then(r => r.json())
        .then(vehicles => {
            vehicles.forEach(v => {
                const opt = document.createElement("option");
                opt.value = v.id;
                opt.textContent = `${v.make} ${v.model}`;
                vehicleSelector.appendChild(opt);
            });
        });

    document.getElementById("tripForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        document.getElementById("loader").classList.remove("hidden");

        const body = {
            from: document.getElementById("from").value,
            to: document.getElementById("to").value,
            vehicle_id: vehicleSelector.value,
            mode: document.getElementById("routeMode").value
        };

        const res = await fetch("/api/plan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });

        const data = await res.json();

        document.getElementById("loader").classList.add("hidden");

        drawRoute(data.coords);
        showChargers(data.stops);

        document.getElementById("distance").textContent = data.distance_km;
        document.getElementById("drive").textContent = data.drive_time_h;
        document.getElementById("charge").textContent = data.charge_time_h;
        document.getElementById("stops").textContent = data.nb_stops;
        document.getElementById("mode").textContent = data.mode;
    });
});

// 🔹 Fonction ajoutée : charger détails véhicule
async function loadVehicleDetails(id) {
    if (!id) return;

    try {
        const res = await fetch(`/api/vehicle/${id}`);
        const data = await res.json();

        const box = document.getElementById("vehicleDetails");
        if (!box) return;

        box.classList.remove("hidden");

        const img = document.getElementById("vehImage");
        if (data.media && data.media.image && data.media.image.url) {
            img.src = data.media.image.url;
            img.style.display = "block";
        } else {
            img.style.display = "none";
        }

        document.getElementById("vehName").textContent =
            (data.naming?.make || "") + " " + (data.naming?.model || "");

        document.getElementById("vehVersion").textContent =
            data.naming?.chargetrip_version || "";

        document.getElementById("vehSpecs").innerHTML = `
            <li><b>Batterie utilisable :</b> ${data.battery?.usable_kwh ?? "-"} kWh</li>
            <li><b>Autonomie (réelle) :</b>
                ${data.range?.chargetrip_range?.worst ?? "-"} –
                ${data.range?.chargetrip_range?.best ?? "-"} km
            </li>
            <li><b>Accélération :</b> ${data.performance?.acceleration ?? "-"} s</li>
            <li><b>Vitesse max :</b> ${data.performance?.top_speed ?? "-"} km/h</li>
            <li><b>Connecteur :</b> ${data.connectors?.[0]?.standard ?? "-"}</li>
            <li><b>Charge rapide :</b>
                ${data.routing?.fast_charging_support ? "Oui" : "Non"}
            </li>
        `;
    } catch (e) {
        console.error("Erreur loadVehicleDetails", e);
    }
}
