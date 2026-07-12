/*
=========================================
 GadiOps API Client
=========================================
*/

const API_BASE_URL = "http://127.0.0.1:8000/api";

async function apiRequest(endpoint, method = "GET", data = null) {

    const token = localStorage.getItem("token");

    const headers = {
        "Content-Type": "application/json"
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const options = {
        method,
        headers
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {

        const response = await fetch(API_BASE_URL + endpoint, options);

        if (response.status === 401) {

            localStorage.clear();

            window.location.href = "login.html";

            return;
        }

        const result = await response.json();

        if (!response.ok) {

            throw new Error(result.detail || "Request failed");

        }

        return result;

    }

    catch (error) {

        console.error(error);

        throw error;

    }

}

const API = {

    get(endpoint) {

        return apiRequest(endpoint);

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