/*
=========================================
 GadiOps Dashboard
=========================================
*/

checkAuth();

/* =========================================
   Dashboard Data
========================================= */

let dashboardData = {};

const demoDashboardData = {

    activeVehicles: 48,

    availableVehicles: 30,

    maintenanceVehicles: 5,

    driversOnDuty: 26,

    activeTrips: 18,

    pendingTrips: 6,

    fleetUtilization: 62

};

let fleetChart = null;

/* =========================================
   Initialize
========================================= */

document.addEventListener("DOMContentLoaded", async () => {

    initializeDarkMode();

    setupRoleUI();

    setupDownloadButton();

    await fetchDashboard();

    const regionFilter =
        document.getElementById("regionFilter");

    const statusFilter =
        document.getElementById("statusFilter");

    if(regionFilter){

        regionFilter.addEventListener(
            "change",
            fetchDashboard
        );

    }

    if(statusFilter){

        statusFilter.addEventListener(
            "change",
            fetchDashboard
        );

    }

});

/* =========================================
   Dashboard API
========================================= */

async function fetchDashboard(){

    try{

        /*
        dashboardData = await API.get("/dashboard");
        */

        dashboardData = demoDashboardData;

        updateDashboard();

    }

    catch(error){

        console.error(error);

        dashboardData = demoDashboardData;

        updateDashboard();

    }

}

/* =========================================
   KPI
========================================= */

function updateDashboard(){

    setValue(
        "activeVehicles",
        dashboardData.activeVehicles
    );

    setValue(
        "availableVehicles",
        dashboardData.availableVehicles
    );

    setValue(
        "maintenanceVehicles",
        dashboardData.maintenanceVehicles
    );

    setValue(
        "driversOnDuty",
        dashboardData.driversOnDuty
    );

    setValue(
        "activeTrips",
        dashboardData.activeTrips
    );

    setValue(
        "pendingTrips",
        dashboardData.pendingTrips
    );

    setValue(
        "fleetUtilization",
        dashboardData.fleetUtilization + "%"
    );

    drawChart();

}

function setValue(id,value){

    const element =
        document.getElementById(id);

    if(element){

        element.textContent=value;

    }

}

/* =========================================
   Chart
========================================= */

function drawChart(){

    const canvas =
        document.getElementById("fleetChart");

    if(!canvas) return;

    if(fleetChart){

        fleetChart.destroy();

    }

    fleetChart =
        new Chart(canvas,{

        type:"doughnut",

        data:{

            labels:[

                "Available",

                "Active",

                "Maintenance"

            ],

            datasets:[{

                data:[

                    dashboardData.availableVehicles,

                    dashboardData.activeTrips,

                    dashboardData.maintenanceVehicles

                ]

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    position:"bottom"

                }

            }

        }

    });

}

/* =========================================
   CSV
========================================= */

function setupDownloadButton(){

    const button =
        document.getElementById("downloadReport");

    if(!button) return;

    button.addEventListener("click",()=>{

        /*
        Backend

        window.location.href=
        API_BASE_URL+"/analytics/export";
        */

        const csv =

`Metric,Value
Active Vehicles,${dashboardData.activeVehicles}
Available Vehicles,${dashboardData.availableVehicles}
Maintenance,${dashboardData.maintenanceVehicles}
Drivers On Duty,${dashboardData.driversOnDuty}
Active Trips,${dashboardData.activeTrips}
Fleet Utilization,${dashboardData.fleetUtilization}%`;

        const blob =
            new Blob([csv],{

                type:"text/csv"

            });

        const link =
            document.createElement("a");

        link.href =
            URL.createObjectURL(blob);

        link.download =
            "dashboard-report.csv";

        link.click();

    });

}

/* =========================================
   Role Based UI
========================================= */

function setupRoleUI(){

    const role =
        localStorage.getItem("role");

    const financial =
        document.getElementById(
            "financialSection"
        );

    const driver =
        document.getElementById(
            "driverPanel"
        );

    if(role==="Driver"){

        if(financial){

            financial.style.display="none";

        }

    }

    if(role==="Financial Analyst"){

        if(driver){

            driver.style.display="none";

        }

    }

}

/* =========================================
   Dark Mode
========================================= */

function initializeDarkMode(){

    const button =
        document.getElementById(
            "darkToggle"
        );

    if(

        localStorage.getItem("theme")
        ==="dark"

    ){

        document.body.classList.add("dark");

    }

    if(!button) return;

    button.addEventListener("click",()=>{

        document.body.classList.toggle("dark");

        if(

            document.body.classList.contains(
                "dark"
            )

        ){

            localStorage.setItem(
                "theme",
                "dark"
            );

        }

        else{

            localStorage.setItem(
                "theme",
                "light"
            );

        }

    });

}