let map;
let routeLayer;
let chargerMarkers = [];
let vehicleSelector = document.getElementById("vehicle");
let themeToggle = document.getElementById("themeToggle");

function initMap() {
    map = L.map('map').setView([46.5, 3], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);
}

async function loadVehicles() {
    const res = await fetch("/api/vehicles");
    const vehicles = await res.json();

    vehicleSelector.innerHTML = "";
    vehicles.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v.id;
        opt.textContent = `${v.make} ${v.model}`;
        vehicleSelector.appendChild(opt);
    });

    // Charger les détails du premier véhicule automatiquement
    if (vehicles.length > 0) {
        loadVehicleDetails(vehicles[0].id);
    }
}


async function loadVehicleDetails(id) {
    const res = await fetch(`/api/vehicle/${id}`);
    const data = await res.json();

    document.getElementById("vehicleDetails").classList.remove("hidden");

    document.getElementById("vehImage").src = data.media.image.url;
    document.getElementById("vehName").textContent =
        `${data.naming.make} ${data.naming.model}`;
    document.getElementById("vehVersion").textContent =
        data.naming.chargetrip_version || "";

    const specs = document.getElementById("vehSpecs");
    specs.innerHTML = `
        <li><b>Batterie utilisable :</b> ${data.battery.usable_kwh} kWh</li>
        <li><b>Autonomie (réelle) :</b> ${data.range.chargetrip_range.worst} - ${data.range.chargetrip_range.best} km</li>
        <li><b>Accélération :</b> ${data.performance.acceleration || "-"} s</li>
        <li><b>Vitesse max :</b> ${data.performance.top_speed || "-"} km/h</li>
        <li><b>Connecteur :</b> ${data.connectors[0].standard}</li>
        <li><b>Charge rapide :</b> ${data.routing.fast_charging_support ? "Oui" : "Non"}</li>
    `;
}


function clearChargerMarkers() {
    chargerMarkers.forEach(m => map.removeLayer(m));
    chargerMarkers = [];
}

function showChargerMarkers(stops) {
    clearChargerMarkers();
    stops.forEach(stop => {
        const marker = L.marker([stop.lat, stop.lon]).addTo(map);
        marker.bindPopup(
            `<b>Borne recommandée</b><br>
             ${stop.name || "Borne"}<br>
             Charge estimée : ${stop.expected_charge_min} min`
        );
        chargerMarkers.push(marker);
    });
}

function animateRoute(coords) {
    if (routeLayer) map.removeLayer(routeLayer);

    routeLayer = L.polyline([], { color: "blue", weight: 5 }).addTo(map);

    let i = 0;
    const interval = setInterval(() => {
        if (i >= coords.length) {
            clearInterval(interval);
            return;
        }
        routeLayer.addLatLng(coords[i]);
        i++;
    }, 20);
}

function animateVehicle(coords) {
    let marker = L.marker(coords[0]).addTo(map);

    let i = 0;
    const interval = setInterval(() => {
        if (i >= coords.length) {
            clearInterval(interval);
            return;
        }
        marker.setLatLng(coords[i]);
        i++;
    }, 40);
}

function renderTimeline(data) {
    const cont = document.getElementById("timeline");
    cont.innerHTML = "";

    const driveWidth = data.drive_time_h * 10;
    const chargeWidth = data.charge_time_h * 10;

    const driveBar = document.createElement("div");
    driveBar.className = "timeline-bar bg-blue-600";
    driveBar.style.width = `${driveWidth}px`;

    const chargeBar = document.createElement("div");
    chargeBar.className = "timeline-bar bg-green-600";
    chargeBar.style.width = `${chargeWidth}px`;

    cont.appendChild(driveBar);
    cont.appendChild(chargeBar);
}

document.getElementById("tripForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    document.getElementById("loader").classList.remove("hidden");

    const from = document.getElementById("from").value.split(',').map(Number);
    const to = document.getElementById("to").value.split(',').map(Number);
    const vehicle = document.getElementById("vehicle").value;

    const body = {
        from_coord: [from[0], from[1]],
        to_coord: [to[0], to[1]],
        vehicle_id: vehicle
    };

    const res = await fetch("/api/plan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });
    const data = await res.json();

    document.getElementById("loader").classList.add("hidden");

    document.getElementById("result").textContent = JSON.stringify(data, null, 2);

    animateRoute(data.coords);
    animateVehicle(data.coords);
    showChargerMarkers(data.stops);
    renderTimeline(data);
});

themeToggle.addEventListener("click", () => {
    document.getElementById("root").classList.toggle("dark");
});

window.onload = () => {
    initMap();
    loadVehicles();
};

vehicleSelector.addEventListener("change", () => {
    loadVehicleDetails(vehicleSelector.value);
});
