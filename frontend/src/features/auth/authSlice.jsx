import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { authApi } from "../../api/authApi";

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ username, password }, thunkAPI) => {
    try {
      const tokenRes = await authApi.login(username, password);
      const { access, refresh } = tokenRes.data;

      const userRes = await authApi.getMe(access);

      return { access, refresh, user: userRes.data };
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data || { detail: "Login failed" }
      );
    }
  }
);

export const signupUser = createAsyncThunk(
  "auth/signupUser",
  async (formData, thunkAPI) => {
    try {
      await authApi.signup(formData);

      const tokenRes = await authApi.login(formData.username, formData.password);
      const { access, refresh } = tokenRes.data;

      const userRes = await authApi.getMe(access);

      return { access, refresh, user: userRes.data };
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data || { detail: "Signup failed" }
      );
    }
  }
);

const loadState = () => {
  try {
    return {
      user: JSON.parse(sessionStorage.getItem("user")),
      accessToken: sessionStorage.getItem("access"),
      refreshToken: sessionStorage.getItem("refresh"),
    };
  } catch {
    return { user: null, accessToken: null, refreshToken: null };
  }
};

const saved = loadState();

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: saved.user,
    accessToken: saved.accessToken,
    refreshToken: saved.refreshToken,
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.loading = false;
      state.error = null;
      sessionStorage.clear();
    },
    updateTokens: (state, action) => {
      state.accessToken = action.payload.access;
      if (action.payload.refresh) {
        state.refreshToken = action.payload.refresh;
      }
      sessionStorage.setItem("access", action.payload.access);
      if (action.payload.refresh) {
        sessionStorage.setItem("refresh", action.payload.refresh);
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    const handlePending = (state) => {
      state.loading = true;
      state.error = null;
    };

    const handleFulfilled = (state, action) => {
      state.loading = false;
      state.user = action.payload.user;
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;

      sessionStorage.setItem("access", action.payload.access);
      sessionStorage.setItem("refresh", action.payload.refresh);
      sessionStorage.setItem("user", JSON.stringify(action.payload.user));
    };

    const handleRejected = (state, action) => {
      state.loading = false;
      state.error = action.payload;
    };

    builder
      .addCase(loginUser.pending, handlePending)
      .addCase(loginUser.fulfilled, handleFulfilled)
      .addCase(loginUser.rejected, handleRejected)
      .addCase(signupUser.pending, handlePending)
      .addCase(signupUser.fulfilled, handleFulfilled)
      .addCase(signupUser.rejected, handleRejected);
  },
});

export const { logout, updateTokens, clearError } = authSlice.actions;
export default authSlice.reducer;
