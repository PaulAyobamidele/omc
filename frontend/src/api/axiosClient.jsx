// src/api/axiosClient.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: false,
});

// We will inject the Redux store after it's created to avoid circular import
let reduxStore = null;

export const injectStore = (store) => {
  reduxStore = store;
};

// REQUEST INTERCEPTOR
api.interceptors.request.use(
  (config) => {
    if (!reduxStore) return config; // store isn't ready yet

    const access = reduxStore.getState().auth.accessToken;

    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }

    config.headers["Content-Type"] = "application/json";
    return config;
  },
  (error) => Promise.reject(error)
);

// RESPONSE INTERCEPTOR (auto refresh token)
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    if (!reduxStore) return Promise.reject(error);

    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = reduxStore.getState().auth.refreshToken;

        const refreshResponse = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh }
        );

        const newAccess = refreshResponse.data.access;

        reduxStore.dispatch({
          type: "auth/updateTokens",
          payload: { access: newAccess },
        });

        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;
        api.defaults.headers.common["Authorization"] = `Bearer newAccess`;

        return api(originalRequest);
      } catch (err) {
        reduxStore.dispatch({ type: "auth/logout" });
      }
    }

    return Promise.reject(error);
  }
);

export default api;
