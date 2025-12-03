// src/store/store.jsx
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import studentReducer from "../features/student/studentSlice";
import { injectStore } from "../api/axiosClient";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    students: studentReducer,
  },
});

// Inject store AFTER it is created
injectStore(store);

export default store;
