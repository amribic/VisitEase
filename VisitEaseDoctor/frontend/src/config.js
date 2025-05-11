// Get the current environment
const isDevelopment = import.meta.env.DEV;

// API URL configuration
const config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  // Add other configuration variables here
};

// CORS configuration
export const CORS_CONFIG = {
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  mode: 'cors'
};

// Helper function for making API calls
export const fetchWithConfig = async (endpoint, options = {}) => {
  try {
    console.log('Making API call to:', `${config.apiUrl}${endpoint}`);
    const response = await fetch(`${config.apiUrl}${endpoint}`, {
      ...CORS_CONFIG,
      ...options,
      headers: {
        ...CORS_CONFIG.headers,
        ...(options.headers || {})
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      console.error('API call failed:', {
        status: response.status,
        statusText: response.statusText,
        error: errorData
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

export default config; 