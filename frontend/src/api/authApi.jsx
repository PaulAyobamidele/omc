import api from "./axiosClient";

export const authApi = {
  login: (username, password) =>
    api.post("/token/", { username, password }),

  signup: (data) =>
    api.post("/users/signup/", data),

  refreshToken: (refresh) =>
    api.post("/token/refresh/", { refresh }),

  getMe: (token) =>
    api.get("/users/me/", token ? { headers: { Authorization: `Bearer ${token}` } } : {}),
};