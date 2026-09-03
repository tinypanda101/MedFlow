/* 
    Single shared Axios instance that every component uses to talk to FastAPI backend
*/

import axios from 'axios';

// Axios.create is a function that builds a reusable pre-configed client
const apiClient = axios.create({
    baseURL: 'http://localhost:8000', // FastAPI backend URL
});

//Request interceptor runs on every outing request and checks if a token exists in local storage
// If so attaches it as Auth header automatically.
// This is centralized place for token logic instead of it being seperate
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('medflowToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});


export default apiClient;