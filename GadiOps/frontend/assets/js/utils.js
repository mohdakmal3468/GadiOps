/*
=========================================
 GadiOps Utilities
=========================================
*/

/* =========================================
   CSV Export
========================================= */

function exportToCSV(data, filename = "analytics.csv") {

    if (!data || data.length === 0) {

        alert("No data available.");

        return;

    }

    const headers = Object.keys(data[0]);

    let csv = headers.join(",") + "\n";

    data.forEach(row => {

        const values = headers.map(header => {

            return `"${String(row[header] ?? "").replace(/"/g,'""')}"`;

        });

        csv += values.join(",") + "\n";

    });

    const blob = new Blob([csv], {

        type:"text/csv;charset=utf-8;"

    });

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

}

/* =========================================
   Expense Management
========================================= */

let expenseData = [];

const expenseVehicles = [

    "Truck-101",
    "Van-205",
    "Bus-301"

];

/* =========================================
   Page Load
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const vehicleSelect = document.getElementById("vehicle");

    if (!vehicleSelect) return;

    loadExpenseVehicles();

    loadExpenseTable();

    document
        .getElementById("expenseForm")
        .addEventListener("submit", addExpense);

    document
        .getElementById("exportBtn")
        .addEventListener("click", () => {

            exportToCSV(expenseData,"expenses.csv");

        });

});

/* =========================================
   Load Vehicles
========================================= */

function loadExpenseVehicles(){

    const select = document.getElementById("vehicle");

    select.innerHTML = `
        <option value="">
            Select Vehicle
        </option>
    `;

    expenseVehicles.forEach(vehicle=>{

        select.innerHTML += `
            <option value="${vehicle}">
                ${vehicle}
            </option>
        `;

    });

}

/* =========================================
   Add Expense
========================================= */

function addExpense(e){

    e.preventDefault();

    const vehicle =
        document.getElementById("vehicle").value;

    const type =
        document.getElementById("expenseType").value;

    const amount =
        document.getElementById("amount").value;

    const fuel =
        document.getElementById("fuelQuantity").value;

    const odometer =
        document.getElementById("odometerReading").value;

    const date =
        document.getElementById("expenseDate").value;

    const description =
        document.getElementById("description").value;

    if(!vehicle || !type || !amount || !date){

        alert("Please fill all required fields.");

        return;

    }

    expenseData.push({

        Vehicle: vehicle,

        Type: type,

        Amount: amount,

        Fuel: fuel || "-",

        Odometer: odometer || "-",

        Date: date,

        Description: description || "-"

    });

    loadExpenseTable();

    document
        .getElementById("expenseForm")
        .reset();

}


function loadExpenseTable(){

    const tbody =
        document.getElementById("expenseTableBody");

    if(!tbody) return;

    tbody.innerHTML = "";

    expenseData.forEach(item=>{

        tbody.innerHTML += `

<tr>

    <td>${item.Vehicle}</td>

    <td>${item.Type}</td>

    <td>₹${item.Amount}</td>

    <td>${item.Fuel}</td>

    <td>${item.Odometer}</td>

    <td>${item.Date}</td>

    <td>${item.Description}</td>

</tr>

`;

    });

}

/* =========================================
   Vehicle Registry
========================================= */

let vehicleRegistry = [];

const demoVehicleRegistry = [

    {
        registration: "UP78AB1234",
        name: "Truck-101",
        type: "Truck",
        capacity: 5000,
        odometer: 12500,
        cost: 950000,
        status: "Available"
    }

];

/* =========================================
   Driver Registry
========================================= */

let driverRegistry = [];

const demoDriverRegistry = [

    {
        name: "Alex",
        license: "DL12345678",
        category: "HMV",
        expiry: "2027-12-31",
        contact: "9876543210",
        safety: 96,
        status: "Available"
    }

];

/* =========================================
   Vehicle & Driver Page Loader
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("vehicleForm")) {

        loadVehicleRegistry();

        renderVehicleTable();

        document
            .getElementById("vehicleForm")
            .addEventListener("submit", registerVehicle);

    }

    if (document.getElementById("driverForm")) {

        loadDriverRegistry();

        renderDriverTable();

        document
            .getElementById("driverForm")
            .addEventListener("submit", registerDriver);

    }

});

/* =========================================
   Vehicle Functions
========================================= */

function loadVehicleRegistry() {

    /*
    Backend

    vehicleRegistry = await API.get("/vehicles");
    */

    vehicleRegistry = demoVehicleRegistry;

}

function registerVehicle(event) {

    event.preventDefault();

    vehicleRegistry.push({

        registration:
            document.getElementById("registrationNumber").value,

        name:
            document.getElementById("vehicleName").value,

        type:
            document.getElementById("vehicleType").value,

        capacity:
            document.getElementById("capacity").value,

        odometer:
            document.getElementById("odometer").value,

        cost:
            document.getElementById("cost").value,

        status:
            document.getElementById("vehicleStatus").value

    });

    renderVehicleTable();

    event.target.reset();

}

function renderVehicleTable() {

    const tbody =
        document.getElementById("vehicleTableBody");

    if (!tbody) return;

    tbody.innerHTML = "";

    vehicleRegistry.forEach(vehicle => {

        tbody.innerHTML += `

        <tr>

            <td>${vehicle.registration}</td>

            <td>${vehicle.name}</td>

            <td>${vehicle.type}</td>

            <td>${vehicle.capacity} Kg</td>

            <td>${vehicle.odometer} Km</td>

            <td>

                <span class="status">

                    ${vehicle.status}

                </span>

            </td>

        </tr>

        `;

    });

}

/* =========================================
   Driver Functions
========================================= */

function loadDriverRegistry() {

    /*
    Backend

    driverRegistry = await API.get("/drivers");
    */

    driverRegistry = demoDriverRegistry;

}

function registerDriver(event) {

    event.preventDefault();

    driverRegistry.push({

        name:
            document.getElementById("driverName").value,

        license:
            document.getElementById("licenseNumber").value,

        category:
            document.getElementById("licenseCategory").value,

        expiry:
            document.getElementById("licenseExpiry").value,

        contact:
            document.getElementById("contactNumber").value,

        safety:
            document.getElementById("safetyScore").value,

        status:
            document.getElementById("driverStatus").value

    });

    renderDriverTable();

    event.target.reset();

}

function renderDriverTable() {

    const tbody =
        document.getElementById("driverTableBody");

    if (!tbody) return;

    tbody.innerHTML = "";

    driverRegistry.forEach(driver => {

        const expired =
            new Date(driver.expiry) < new Date();

        tbody.innerHTML += `

        <tr>

            <td>${driver.name}</td>

            <td>${driver.license}</td>

            <td>${driver.category}</td>

            <td style="color:${expired ? "red" : "inherit"}">

                ${driver.expiry}

            </td>

            <td>${driver.contact}</td>

            <td>${driver.safety}</td>

            <td>

                <span class="status">

                    ${driver.status}

                </span>

            </td>

        </tr>

        `;

    });

}

/* =========================================
   Phase 4 : Maintenance Module
========================================= */

let maintenanceLogs = [];

/* =========================================
   Open Modal
========================================= */

function openMaintenanceModal(index){

    document
        .getElementById("maintenanceVehicleIndex")
        .value = index;

    document
        .getElementById("maintenanceModal")
        .classList
        .add("active");

}

/* =========================================
   Close Modal
========================================= */

function closeMaintenanceModal(){

    document
        .getElementById("maintenanceModal")
        .classList
        .remove("active");

    document
        .getElementById("maintenanceForm")
        .reset();

}

/* =========================================
   Save Maintenance
========================================= */

const maintenanceForm =
    document.getElementById("maintenanceForm");

if(maintenanceForm){

    maintenanceForm.addEventListener(
        "submit",
        saveMaintenance
    );

}

function saveMaintenance(event){

    event.preventDefault();

    const index = Number(
        document.getElementById(
            "maintenanceVehicleIndex"
        ).value
    );

    const type =
        document.getElementById(
            "maintenanceType"
        ).value;

    const cost =
        document.getElementById(
            "maintenanceCost"
        ).value;

    const note =
        document.getElementById(
            "maintenanceNote"
        ).value;

    maintenanceLogs.push({

        vehicle:
            vehicleRegistry[index].registration,

        type,

        cost,

        note,

        date:
            new Date()
                .toLocaleDateString()

    });

    vehicleRegistry[index].status =
        "In Shop";

    /*
    ================================
    Backend Ready

    await API.post(
        "/maintenance",
        maintenanceLogs[
            maintenanceLogs.length-1
        ]
    );

    await API.put(
        `/vehicles/${vehicleRegistry[index].id}`,
        {
            status:"In Shop"
        }
    );
    ================================
    */

    renderVehicleTable();

    closeMaintenanceModal();

}

/* =========================================
   Vehicle Table Update
========================================= */

const oldRenderVehicleTable =
    renderVehicleTable;

renderVehicleTable = function(){

    const tbody =
        document.getElementById(
            "vehicleTableBody"
        );

    if(!tbody) return;

    tbody.innerHTML="";

    vehicleRegistry.forEach(
        (vehicle,index)=>{

        let badge="status";

        switch(vehicle.status){

            case "Available":

                badge+=" status-available";

                break;

            case "On Trip":

                badge+=" status-trip";

                break;

            case "In Shop":

                badge+=" status-shop";

                break;

            default:

                badge+=" status-retired";

        }

        tbody.innerHTML += `

<tr>

<td>${vehicle.registration}</td>

<td>${vehicle.name}</td>

<td>${vehicle.type}</td>

<td>${vehicle.capacity} Kg</td>

<td>${vehicle.odometer} Km</td>

<td>

<span class="${badge}">

${vehicle.status}

</span>

</td>

<td>

<button
class="shop-btn"
onclick="openMaintenanceModal(${index})"

${vehicle.status==="In Shop" ? "disabled" : ""}>

Send To Shop

</button>

</td>

</tr>

`;

    });

};