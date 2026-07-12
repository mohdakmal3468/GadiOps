/*
=========================================
 GadiOps - Global API Client
 Author: Team GadiOps
=========================================
*/

const API_BASE_URL = "http://127.0.0.1:8000/api"; // Change if backend uses another URL

/**
 * Generic API Request
 * @param {string} endpoint
 * @param {string} method
 * @param {object|null} data
 * @returns JSON Response
 */
async function apiRequest(endpoint, method = "GET", data = null) {

    // Read JWT Token
    const token = localStorage.getItem("token");

    // Default Headers
    const headers = {
        "Content-Type": "application/json"
    };

    // Add Authorization Header
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers
    };

    // Attach Body for POST/PUT
    if (data) {
        options.body = JSON.stringify(data);
    }

    try {

        const response = await fetch(API_BASE_URL + endpoint, options);

        // Unauthorized
        if (response.status === 401) {

            localStorage.removeItem("token");
            localStorage.removeItem("role");
            localStorage.removeItem("username");

            window.location.href = "/templates/login.html";
            return;
        }

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Something went wrong");
        }

        return result;

    } catch (error) {

        console.error("API Error:", error);

        throw error;
    }
}

/* =======================================
   Shortcut Methods
======================================= */

const API = {

    get(endpoint) {
        return apiRequest(endpoint, "GET");
    },

    post(endpoint, data) {
        return apiRequest(endpoint, "POST", data);
    },

    put(endpoint, data) {
        return apiRequest(endpoint, "PUT", data);
    },

    delete(endpoint) {
        return apiRequest(endpoint, "DELETE");
    }

};