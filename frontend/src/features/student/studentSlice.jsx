import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axiosClient.jsx";
import { createStudentApi } from "./studentApi.jsx";


export const fetchParentStudents = createAsyncThunk(
  "students/fetchParentStudents",
  async (_, thunkAPI) => {
    try {
      const response = await api.get("/grades/parent/"); 
      const students = response.data.map((g) => g.student);
      return students;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || "Error fetching students");
    }
  }
);

export const createStudent = createAsyncThunk(
  "students/createStudent",
  async (studentData, thunkAPI) => {
    try {
      const result = await createStudentApi(studentData);
      return result;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || "Error creating student");
    }
  }
)

const studentSlice = createSlice({
  name: "students",
  initialState: {
    list: [],
    loading: false,
    error: null,
    createLoading: false,
    createError: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchParentStudents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchParentStudents.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchParentStudents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    builder
      .addCase(createStudent.pending, (state) => {
        state.createLoading = true;
        state.createError = null;
      })
      .addCase(createStudent.fulfilled, (state, action) => {
        state.createLoading = false;
        state.list.push(action.payload);
      })
      .addCase(createStudent.rejected, (state, action) => {
        state.createLoading = false;
        state.createError = action.payload;
      });
  },
});

export default studentSlice.reducer;
