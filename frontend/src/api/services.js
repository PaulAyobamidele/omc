import api from "./axiosClient";

export const studentsApi = {
  list: (params) => api.get("/students/", { params }),
  byClass: (classId) => api.get(`/students/by-class/${classId}/`),
  create: (data) => api.post("/students/create/", data),
};

export const gradesApi = {
  enter: (data) => api.post("/grades/enter/", data),
  update: (id, data) => api.patch(`/grades/${id}/update/`, data),
  studentGrades: (params) => api.get("/grades/student/", { params }),
  parentGrades: (params) => api.get("/grades/parent/", { params }),
  classGrades: (classId, params) => api.get(`/grades/class/${classId}/`, { params }),
  subjectGrades: (subjectId, params) => api.get(`/grades/subject/${subjectId}/`, { params }),
  studentSummary: (studentId, params) => api.get(`/grades/student/${studentId}/summary/`, { params }),
  classSummary: (classId, params) => api.get(`/grades/class/${classId}/summary/`, { params }),
};

export const classesApi = {
  list: () => api.get("/classes/school-classes/"),
  detail: (id) => api.get(`/classes/school-classes/${id}/`),
  classSubjects: (params) => api.get("/classes/class-subjects/", { params }),
  createClassSubject: (data) => api.post("/classes/class-subjects/", data),
  sessions: () => api.get("/classes/sessions/"),
  terms: (params) => api.get("/classes/terms/", { params }),
  activeTerm: () => api.get("/classes/terms/active/"),
};

export const subjectsApi = {
  list: () => api.get("/subjects/"),
  detail: (id) => api.get(`/subjects/${id}/`),
};

export const parentsApi = {
  list: (params) => api.get("/parents/", { params }),
};

export const teachersApi = {
  list: () => api.get("/teachers/"),
  dashboard: () => api.get("/teachers/dashboard/"),
};

export const reportsApi = {
  studentReport: (studentId, params) => api.get(`/reports/student/${studentId}/`, { params }),
};
