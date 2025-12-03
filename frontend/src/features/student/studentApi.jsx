import api from "../../api/axiosClient.jsx";

export const createStudentApi = async (studentData) => {
  const response = await api.post("/students/create/", studentData);
  return response.data; // returns { student_id, username, password, class_level }
};

export const fetchParentStudentsApi = async () => {
  const response = await api.get("/grades/parent/");
  return response.data.map((g) => g.student);
};
