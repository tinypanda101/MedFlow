/*
    Global Auth state using React's context API
*/

import {createContext, useContext, useMemo, useState} from 'react';
import apiClient from "../api/client";

// Create a global react context that acts as a central store for auth state without manual prop pass
const AuthContext = createContext(null);

//Extract and decode the user payload from JWT so that React cna read it
function decodeToken(token) {
    const payloadSegment = token.split('.')[1];
    return JSON.parse(atob(payloadSegment));
}

//AuthProvider is a component that wraps the app and manages auth state
export function AuthProvider({ children }) {
    // Initalizing our token state from local storage to ensure a user stays logged in
    const [token, setToken] = useState(() => localStorage.getItem('medflowToken'));

    // Decode JWT into user object and cache the results
    const user = useMemo(() => (token ? decodeToken(token): null), [token]);

    //Authenticates user credentials against backend API by sending credentials, saving returned token to local storage and updating react state
    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        });

        localStorage.setItem('medflowToken', response.data.access_token);
        setToken(response.data.access_token);
    };


    //logout function clears the token from local storage and updates react state
    const logout = () => {
        localStorage.removeItem('medflowToken');
        setToken(null);
    };

    //Bundles auth state variables and action functions into a single object
    const value = {
        token,
        user,
        isAuthenticated: Boolean(token),
        login,
        logout,
    };

    //Renders the context provider and passes down the value object to make the auth state and functions accessible throughout the app
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

//Custom React hook that exposes the AuthContext to any component
//TLDR simplifies context usage in child React components
// useAuth() instead of useContext(AuthContext) and throws error if used outside AuthProvider
export function useAuth() {
    const context = useContext(AuthContext);
    if (context == null) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}
