// Get the current environment
const isDevelopment = import.meta.env.DEV;

// API URL configuration
export const API_URL = isDevelopment 
  ? (import.meta.env.VITE_API_URL || 'http://localhost:8080')
  : 'https://visitease.onrender.com';

// CORS configuration
export const CORS_CONFIG = {
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  mode: 'cors'
}; 