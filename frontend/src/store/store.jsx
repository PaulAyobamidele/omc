import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import schoolReducer from "../features/schools/schoolSlice";
import { injectStore } from "../api/axiosClient";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    school: schoolReducer,
  },
});

injectStore(store);
export default store;
