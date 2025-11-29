import axios from "axios";
import { store } from "../store/store";
import { logout } from "../features/auth/authSlice";
import { refreshTokenApi } from "./authApi";
// import { useAuthStore } from "../store/authStore";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: false,
});


api.interceptors.request.use(
  (config) => {
    const state = store.getState();
    const access = state.auth.accessToken;


    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }

    config.headers["Content-Type"] = "application/json";
    return config;
  
  },
  (error) => Promise.reject(error)
);
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response) {
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const newTokens = await refreshTokenApi();


          api.defaults.headers.common["Authorization"] = `Bearer ${newTokens.access}`;
          originalRequest.headers["Authorization"] = `Bearer ${newTokens.access}`;

          return api(originalRequest);
        } catch (refreshError) {
          store.dispatch(logout());
        }
      }
    }

    return Promise.reject(error);
  }
);


export default api;