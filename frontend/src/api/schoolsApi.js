import api from "./axiosClient";

export const schoolsApi = {
  register: (data) => api.post("/schools/register/", data),
  getPublic: (slug) => api.get(`/schools/${slug}/public/`),
  update: (slug, data) => api.patch(`/schools/${slug}/`, data),
};
