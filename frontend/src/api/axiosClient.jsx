import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false,
});

let reduxStore = null;

export const injectStore = (store) => {
  reduxStore = store;
};

api.interceptors.request.use(
  (config) => {
    if (!reduxStore) return config;
    const state = reduxStore.getState();
    const access = state.auth.accessToken;
    const slug = state.school?.slug;
    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }
    if (slug) {
      config.headers["X-School-Slug"] = slug;
    }
    config.headers["Content-Type"] = "application/json";
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (!reduxStore) return Promise.reject(error);

    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = reduxStore.getState().auth.refreshToken;
        if (!refresh) throw new Error("No refresh token");

        const response = await axios.post(`${API_BASE}/token/refresh/`, {
          refresh,
        });

        const newAccess = response.data.access;
        const newRefresh = response.data.refresh || refresh;

        reduxStore.dispatch({
          type: "auth/updateTokens",
          payload: { access: newAccess, refresh: newRefresh },
        });

        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;
        return api(originalRequest);
      } catch (refreshError) {
        reduxStore.dispatch({ type: "auth/logout" });
        const slug = reduxStore.getState().school?.slug;
        window.location.href = slug ? `/${slug}/login` : "/";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
