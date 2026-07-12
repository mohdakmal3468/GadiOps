/*
=========================================
 GadiOps Authentication
=========================================
*/

// Redirect if already logged in (Only on login page)
if (
    window.location.pathname.includes("login.html") &&
    localStorage.getItem("token")
) {
    window.location.href = "dashboard.html";
}

// Get Elements
const loginForm = document.getElementById("loginForm");
const loginBtn = document.getElementById("loginBtn");
const errorMessage = document.getElementById("errorMessage");

// Only run login logic if login page exists
if (loginForm) {

    loginForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        errorMessage.textContent = "";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {

            errorMessage.textContent = "Please enter email and password.";

            return;
        }

        loginBtn.disabled = true;
        loginBtn.textContent = "Signing In...";

        try {

            /**********************************************
             DEMO LOGIN
             Replace with backend later
            **********************************************/

            await new Promise(resolve => setTimeout(resolve, 1000));

            localStorage.setItem("token", "demo-jwt-token");
            localStorage.setItem("role", "Fleet Manager");
            localStorage.setItem("username", "Demo User");

            /*
            const response = await API.post("/auth/login", {
                email,
                password
            });

            localStorage.setItem("token", response.access_token);
            localStorage.setItem("role", response.role);
            localStorage.setItem("username", response.name);
            */

            window.location.href = "dashboard.html";

        }

        catch (error) {

            console.error(error);

            errorMessage.textContent =
                error.message || "Invalid email or password.";

        }

        finally {

            loginBtn.disabled = false;
            loginBtn.textContent = "Login";

        }

    });

}

/* =========================================
   Route Guard
========================================= */

function checkAuth() {

    const token = localStorage.getItem("token");

    if (!token) {

        window.location.href = "login.html";

    }

}

/* =========================================
   Logout
========================================= */

function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");

    window.location.href = "login.html";

}