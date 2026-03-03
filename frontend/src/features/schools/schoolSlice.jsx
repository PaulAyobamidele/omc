import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axiosClient";

export const fetchSchoolPublic = createAsyncThunk(
  "school/fetchPublic",
  async (slug, thunkAPI) => {
    try {
      const res = await api.get(`/schools/${slug}/public/`);
      return res.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data || { detail: "School not found." }
      );
    }
  }
);

const schoolSlice = createSlice({
  name: "school",
  initialState: {
    slug: null,
    id: null,
    name: null,
    logoUrl: null,
    primaryColor: "#2563eb",
    address: null,
    phone: null,
    email: null,
    loading: false,
    error: null,
  },
  reducers: {
    setSlug: (state, action) => {
      state.slug = action.payload;
    },
    clearSchool: (state) => {
      state.slug = null;
      state.id = null;
      state.name = null;
      state.logoUrl = null;
      state.primaryColor = "#2563eb";
      state.address = null;
      state.phone = null;
      state.email = null;
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSchoolPublic.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSchoolPublic.fulfilled, (state, action) => {
        state.loading = false;
        const d = action.payload;
        state.id = d.id;
        state.name = d.name;
        state.logoUrl = d.logo_url || null;
        state.primaryColor = d.primary_color || "#2563eb";
        state.address = d.address || null;
        state.phone = d.phone || null;
        state.email = d.email || null;
      })
      .addCase(fetchSchoolPublic.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { setSlug, clearSchool } = schoolSlice.actions;
export default schoolSlice.reducer;
