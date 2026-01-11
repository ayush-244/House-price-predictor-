/**
 * API Service
 * 
 * Handles all API communication with the backend
 */

import axios from 'axios';

// API base URL - can be configured via environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 seconds
});

// Request interceptor for logging
apiClient.interceptors.request.use(
    (config) => {
        console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error) => {
        console.error('API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

/**
 * Predict house price
 * @param {Object} features - House features
 * @returns {Promise} Prediction response
 */
export const predictPrice = async (features) => {
    try {
        const response = await apiClient.post('/predict', features);
        return response.data;
    } catch (error) {
        throw new Error(
            error.response?.data?.detail?.message ||
            error.response?.data?.message ||
            'Failed to get prediction. Please try again.'
        );
    }
};

/**
 * Check API health
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
    try {
        const response = await apiClient.get('/health');
        return response.data;
    } catch (error) {
        throw new Error('Failed to check API health');
    }
};

/**
 * Get form dropdown options
 */
export const getOptions = async () => {
    try {
        const response = await apiClient.get('/options');
        return response.data;
    } catch (error) {
        console.error("Failed to load options:", error);
        return { locations: {}, property_types: [] };
    }
};

/**
 * Get model information
 * @returns {Promise} Model info
 */
export const getModelInfo = async () => {
    try {
        const response = await apiClient.get('/model-info');
        return response.data;
    } catch (error) {
        throw new Error('Failed to get model information');
    }
};

export default apiClient;
