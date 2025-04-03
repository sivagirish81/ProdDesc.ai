import axios from 'axios';

// Create axios instance with base URL from environment variable
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Clear token and redirect to login
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// API endpoints
export const fetchProducts = async () => {
  try {
    const response = await api.get('/api/products');
    // Ensure we return an array, even if the API returns a different structure
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching products:', error);
    return []; // Return empty array on error
  }
};

export const fetchProduct = (id) => api.get(`/api/products/${id}`);
export const generateContent = (productId) => api.post(`/api/content/generate/${productId}`);
export const completeProduct = (productId) => api.post(`/api/content/complete/${productId}`);
export const generateProductImages = (productId) => api.post(`/api/content/generate-images/${productId}`);

export default api;