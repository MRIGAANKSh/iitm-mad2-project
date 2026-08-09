
import axios from "axios";


// =====================================================
// AXIOS INSTANCE
// =====================================================

const api = axios.create({

  baseURL: "http://127.0.0.1:5000/api",

  headers: {
    "Content-Type": "application/json",
  },

});


// =====================================================
// REQUEST INTERCEPTOR
// Attach JWT token to every request
// =====================================================

api.interceptors.request.use(

  (config) => {

    const token =
      localStorage.getItem("token");


    console.log(
      "API Request:",
      config.method?.toUpperCase(),
      config.url
    );

    console.log(
      "Token:",
      token
        ? "JWT token exists"
        : "NO TOKEN"
    );


    if (token) {

      config.headers =
        config.headers || {};

      config.headers.Authorization =
        `Bearer ${token}`;

    }


    return config;

  },

  (error) => {

    return Promise.reject(error);

  }

);


// =====================================================
// RESPONSE INTERCEPTOR
// =====================================================

api.interceptors.response.use(

  (response) => {

    return response;

  },


  (error) => {

    const status =
      error?.response?.status;


    // =================================================
    // 401 UNAUTHORIZED
    // =================================================

    if (status === 401) {

      console.error(
        "401 Unauthorized"
      );


      console.error(
        "API:",
        error?.config?.url
      );


      console.error(
        "Response:",
        error?.response?.data
      );


      /*
       * Do NOT automatically delete the token here.
       *
       * This makes debugging JWT problems easier.
       *
       * If the token is actually expired/invalid,
       * the backend will tell us through the response.
       */

    }


    // =================================================
    // 403 FORBIDDEN
    // =================================================

    if (status === 403) {

      console.error(
        "403 Forbidden - Access denied."
      );


      console.error(
        "API:",
        error?.config?.url
      );


      console.error(
        "Response:",
        error?.response?.data
      );

    }


    // =================================================
    // 400 BAD REQUEST
    // =================================================

    if (status === 400) {

      console.error(
        "400 Bad Request"
      );


      console.error(
        "API:",
        error?.config?.url
      );


      console.error(
        "Response:",
        error?.response?.data
      );

    }


    // =================================================
    // 500 SERVER ERROR
    // =================================================

    if (status >= 500) {

      console.error(
        "500 Server Error"
      );


      console.error(
        "API:",
        error?.config?.url
      );


      console.error(
        "Response:",
        error?.response?.data
      );

    }


    return Promise.reject(error);

  }

);


export default api;

