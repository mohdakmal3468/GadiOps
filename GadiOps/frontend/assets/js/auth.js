/*
=========================================
 GadiOps Authentication
=========================================
*/

/* =========================================
   Login Redirect
========================================= */

if (

    window.location.pathname.includes("login.html") &&

    localStorage.getItem("token")

){

    window.location.href="dashboard.html";

}

/* =========================================
   Login
========================================= */

const loginForm =
    document.getElementById("loginForm");

if(loginForm){

    loginForm.addEventListener(

        "submit",

        login

    );

}

async function login(event){

    event.preventDefault();

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try{

        /*
        Backend

        const response =
            await API.post("/auth/login",{

                email,

                password

            });

        */

        const response={

            access_token:"demo-token",

            role:"Fleet Manager",

            name:"Demo User"

        };

        localStorage.setItem(

            "token",

            response.access_token

        );

        localStorage.setItem(

            "role",

            response.role

        );

        localStorage.setItem(

            "username",

            response.name

        );

        window.location.href="dashboard.html";

    }

    catch(error){

        alert("Login Failed");

        console.error(error);

    }

}

/* =========================================
   Route Guard
========================================= */

function checkAuth(){

    if(

        !localStorage.getItem("token")

    ){

        window.location.href="login.html";

    }

    applyRoleVisibility();

    applyTheme();

}

/* =========================================
   Role UI
========================================= */

function applyRoleVisibility(){

    const role=

        localStorage.getItem("role");

    const financial=

        document.getElementById(

            "financialSection"

        );

    const driver=

        document.getElementById(

            "driverPanel"

        );

    if(

        role==="Driver"

    ){

        if(financial){

            financial.style.display="none";

        }

    }

    if(

        role==="Financial Analyst"

    ){

        if(driver){

            driver.style.display="none";

        }

    }

}

/* =========================================
   Theme
========================================= */

function applyTheme(){

    if(

        localStorage.getItem("theme")==="dark"

    ){

        document.body.classList.add("dark");

    }

}

/* =========================================
   Logout
========================================= */

function logout(){

    localStorage.clear();

    window.location.href="login.html";

}