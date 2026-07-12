/*
=========================================
 GadiOps Dashboard
=========================================
*/

checkAuth();

/* =========================================
   Demo Dashboard Data
========================================= */

let dashboardData = {
    activeVehicles: 48,
    availableVehicles: 30,
    maintenanceVehicles: 5,
    driversOnDuty: 26,
    activeTrips: 18,
    pendingTrips: 6,
    fleetUtilization: 62
};

/* =========================================
   Load Dashboard
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    loadDashboard();

    document
        .getElementById("regionFilter")
        .addEventListener("change", applyFilters);

    document
        .getElementById("statusFilter")
        .addEventListener("change", applyFilters);

});

/* =========================================
   Display KPI Cards
========================================= */

function loadDashboard() {

    document.getElementById("activeVehicles").textContent =
        dashboardData.activeVehicles;

    document.getElementById("availableVehicles").textContent =
        dashboardData.availableVehicles;

    document.getElementById("maintenanceVehicles").textContent =
        dashboardData.maintenanceVehicles;

    document.getElementById("driversOnDuty").textContent =
        dashboardData.driversOnDuty;

    document.getElementById("activeTrips").textContent =
        dashboardData.activeTrips;

    document.getElementById("pendingTrips").textContent =
        dashboardData.pendingTrips;

    document.getElementById("fleetUtilization").textContent =
        dashboardData.fleetUtilization + "%";

    drawChart();

}

/* =========================================
   Filters (Demo)
========================================= */

function applyFilters() {

    const region = document.getElementById("regionFilter").value;
    const status = document.getElementById("statusFilter").value;

    console.log("Region:", region);
    console.log("Status:", status);

    /*
    Backend Integration

    const data = await API.get(
        `/dashboard?region=${region}&status=${status}`
    );

    dashboardData = data;

    loadDashboard();
    */

}

/* =========================================
   Fleet Chart
========================================= */

let fleetChart;

function drawChart() {

    const ctx = document
        .getElementById("fleetChart")
        .getContext("2d");

    if (fleetChart) {
        fleetChart.destroy();
    }

    fleetChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [

                "Available",
                "On Trip",
                "Maintenance"

            ],

            datasets: [

                {

                    data: [

                        dashboardData.availableVehicles,
                        dashboardData.activeTrips,
                        dashboardData.maintenanceVehicles

                    ]

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}