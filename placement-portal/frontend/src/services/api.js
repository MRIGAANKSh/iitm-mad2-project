
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});


// Attach JWT token to every request
api.interceptors.request.use(
  (config) => {

    const token = localStorage.getItem("token");

    console.log("Token:", token);

    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);


// Handle API responses
api.interceptors.response.use(
  (response) => {
    return response;
  },

  (error) => {

    if (error.response?.status === 401) {

      console.error(
        "Unauthorized request:",
        error.response?.data
      );

      console.error(
        "Request:",
        error.config?.url
      );

      // Don't remove the token automatically.
      // First check whether the token is actually valid.
    }

    return Promise.reject(error);
  }
);


export default api;

