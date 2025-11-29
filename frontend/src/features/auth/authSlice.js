import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import axios from 'axios';

// export const loginUser = createAsyncThunk(
//     'auth/loginUser',
//     async ({username, password}, thunkAPI) => {
//         try {
//             const response = await axios.post('http://localhost:8000/api/token/', { username, password });
//             return response.data;
//         } catch (error) {
//             return thunkAPI.rejectWithValue(error.response.data);
//         }
//     }
// );


export const loginUser = createAsyncThunk(
    'auth/loginUser',
    async ({ username, password }, thunkAPI) => {
        try {
            // 1. Get access + refresh tokens
            const tokenResponse = await axios.post(
                "http://localhost:8000/api/token/",
                { username, password }
            );

            const { access, refresh } = tokenResponse.data;

            // 2. Fetch user profile using the access token
            const userResponse = await axios.get(
                "http://localhost:8000/api/users/me/",
                {
                    headers: {
                        Authorization: `Bearer ${access}`
                    }
                }
            );

            return {
                access,
                refresh,
                user: userResponse.data,
            };

        } catch (error) {
            return thunkAPI.rejectWithValue(error.response?.data || "Login failed");
        }
    }
);


const authSlice = createSlice({
    name: 'auth',
    initialState: {
        user: null,
        accessToken: null,
        refreshToken: null,
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
        },

        updateTokens: (state, action) => {
            state.accessToken = action.payload.access;
            if (action.payload.refresh) {
                state.refreshToken = action.payload.refresh;
            }
        },
    },

    extraReducers: (builder) => {
        builder
            .addCase(loginUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload.user;
                state.accessToken = action.payload.access;
                state.refreshToken = action.payload.refresh;
            })
            .addCase(loginUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || 'Something went wrong';
            });
    },

});


export const { logout, updateTokens } = authSlice.actions;
export default authSlice.reducer;


