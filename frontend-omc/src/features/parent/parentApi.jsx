import api from "../../api/axiosClient.jsx";

export async function fetchParentStudents() {
    const response = await api.get('/grades/parents/');
    return response.data;
}