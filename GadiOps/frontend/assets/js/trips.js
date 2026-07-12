/*
=========================================
 GadiOps Trip Lifecycle
=========================================
*/

checkAuth();

let vehicles = [
    {
        id: 1,
        name: "Truck-101",
        status: "Available",
        capacity: 5000
    },
    {
        id: 2,
        name: "Van-205",
        status: "Available",
        capacity: 1500
    }
];

let drivers = [
    {
        id: 1,
        name: "Alex",
        status: "Available",
        licenseValid: true
    },
    {
        id: 2,
        name: "John",
        status: "Available",
        licenseValid: true
    }
];

let trips = [];

document.addEventListener("DOMContentLoaded", () => {

    loadVehicles();

    loadDrivers();

    renderBoard();

    document
        .getElementById("tripForm")
        .addEventListener("submit", saveDraft);

});

/* =========================================
   Dropdowns
========================================= */

function loadVehicles() {

    const select = document.getElementById("vehicle");

    if (!select) return;

    select.innerHTML =
        '<option value="">Select Vehicle</option>';

    vehicles
        .filter(v => v.status === "Available")
        .forEach(v => {

            select.innerHTML +=
                `<option value="${v.id}">${v.name}</option>`;

        });

}

function loadDrivers() {

    const select = document.getElementById("driver");

    if (!select) return;

    select.innerHTML =
        '<option value="">Select Driver</option>';

    drivers
        .filter(d => d.status === "Available" && d.licenseValid)
        .forEach(d => {

            select.innerHTML +=
                `<option value="${d.id}">${d.name}</option>`;

        });

}

/* =========================================
   Save Draft
========================================= */

function saveDraft(event) {

    event.preventDefault();

    const vehicle =
        vehicles.find(v =>
            v.id == document.getElementById("vehicle").value);

    const driver =
        drivers.find(d =>
            d.id == document.getElementById("driver").value);

    if (!vehicle || !driver) {

        alert("Select vehicle and driver.");

        return;

    }

    const cargo =
        Number(document.getElementById("cargoWeight").value);

    if (cargo > vehicle.capacity) {

        alert("Cargo exceeds vehicle capacity.");

        return;

    }

    trips.push({

        id: Date.now(),

        source:
            document.getElementById("source").value,

        destination:
            document.getElementById("destination").value,

        vehicle,

        driver,

        cargo,

        distance:
            document.getElementById("distance").value,

        status: "Draft"

    });

    document.getElementById("tripForm").reset();

    renderBoard();

}

/* =========================================
   Render Board
========================================= */

function renderBoard() {

    renderColumn("Draft", "draftTrips");

    renderColumn("Dispatched", "dispatchedTrips");

    renderColumn("Completed", "completedTrips");

}

function renderColumn(status, containerId) {

    const container =
        document.getElementById(containerId);

    if (!container) return;

    container.innerHTML = "";

    const filtered =
        trips.filter(t => t.status === status);

    if (filtered.length === 0) {

        container.innerHTML =
            `<div class="empty-column">
                No Trips
            </div>`;

        return;

    }

    filtered.forEach(trip => {

        let buttons = "";

        if (status === "Draft") {

            buttons = `
                <button
                    class="card-btn dispatch-btn"
                    onclick="dispatchTrip(${trip.id})">

                    Dispatch

                </button>
            `;

        }

        if (status === "Dispatched") {

            buttons = `
                <button
                    class="card-btn complete-btn"
                    onclick="completeTrip(${trip.id})">

                    Complete

                </button>

                <button
                    class="card-btn cancel-btn"
                    onclick="cancelTrip(${trip.id})">

                    Cancel

                </button>
            `;

        }

        container.innerHTML += `

        <div class="trip-card">

            <h3>${trip.vehicle.name}</h3>

            <p><strong>Driver:</strong> ${trip.driver.name}</p>

            <p><strong>Route:</strong>
                ${trip.source}
                →
                ${trip.destination}
            </p>

            <p><strong>Cargo:</strong>
                ${trip.cargo} Kg
            </p>

            <div class="card-actions">

                ${buttons}

            </div>

        </div>

        `;

    });

}

/* =========================================
   Lifecycle
========================================= */

function dispatchTrip(id) {

    const trip =
        trips.find(t => t.id === id);

    if (!trip) return;

    trip.status = "Dispatched";

    trip.vehicle.status = "On Trip";

    trip.driver.status = "On Trip";

    loadVehicles();

    loadDrivers();

    renderBoard();

}

function completeTrip(id) {

    const trip =
        trips.find(t => t.id === id);

    if (!trip) return;

    trip.status = "Completed";

    trip.vehicle.status = "Available";

    trip.driver.status = "Available";

    loadVehicles();

    loadDrivers();

    renderBoard();

}

function cancelTrip(id) {

    const index =
        trips.findIndex(t => t.id === id);

    if (index === -1) return;

    trips[index].vehicle.status = "Available";

    trips[index].driver.status = "Available";

    trips.splice(index, 1);

    loadVehicles();

    loadDrivers();

    renderBoard();

}