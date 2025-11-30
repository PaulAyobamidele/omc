import axios from 'axios';

import { store } from '../store/store.jsx';
import {updateTokens} from '../features/auth/authSlice.jsx';


const BASE_URL = "http://localhost:8000/api";

export async function loginApi(username, password){
    const response = await axios.post(`${BASE_URL}/auth/login/`, {
        username,
        password
    });
    return response.data;
}


export async function refreshTokenApi(){
    const state = store.getState();
    const refresh = state.auth.refreshToken;

    const response = await axios.post(`${BASE_URL}/auth/refresh/`, {
        refresh: refresh
    });

    store.dispatch(updateTokens(response.data));

    return response.data;
}