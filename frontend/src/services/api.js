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

export const fetchProduct = async (id) => {
  try {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

export const createProduct = async (productData) => {
  try {
    // Format the request data
    const requestData = {
      name: productData.name,
      price: productData.price,
      brand: productData.brand,
      category: productData.category,
      basic_description: productData.basic_description,
      features: productData.features || [],
      materials: productData.materials || [],
      colors: productData.colors || [],
      tags: productData.tags || []
    };
    
    const response = await api.post('/api/products', requestData);
    return response.data;
  } catch (error) {
    console.error('Error creating product:', error);
    throw error;
  }
};

export const updateProduct = async (id, productData) => {
  try {
    const response = await api.put(`/api/products/${id}`, productData);
    return response.data;
  } catch (error) {
    console.error('Error updating product:', error);
    throw error;
  }
};

export const deleteProduct = async (id) => {
  try {
    await api.delete(`/api/products/${id}`);
    return true;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

export const generateSectionContent = async (id, section, formData) => {
  try {
    const requestBody = {
      section: section,
      form_data: {
        name: formData.name,
        price: formData.price,
        brand: formData.brand,
        category: formData.category,
        basic_description: formData.basic_description,
        features: formData.features || [],
        materials: formData.materials || [],
        colors: formData.colors || [],
        tags: formData.tags || []
      }
    };

    const response = await api.post(`/api/products/${id}/generate`, requestBody);
    return response.data;
  } catch (error) {
    console.error('Error generating content:', error);
    throw error;
  }
};

export const completeProduct = async (id) => {
  try {
    // Extract the numeric ID from the custom ID if needed
    const productId = id.startsWith('custom-') ? parseInt(id.split('-')[1]) : id;
    const response = await api.post(`/api/products/${productId}/complete`);
    return response.data;
  } catch (error) {
    console.error('Error completing product:', error);
    throw error;
  }
};

export const generateProductImages = async (productId, options = {}) => {
  try {
    const response = await api.post(`/api/products/${productId}/images`, options);
    return response.data;
  } catch (error) {
    console.error('Error generating images:', error);
    throw error;
  }
};

export const updateProductImage = async (productId, imageData) => {
  try {
    const response = await api.put(`/api/products/${productId}/image`, imageData);
    return response.data;
  } catch (error) {
    console.error('Error updating product image:', error);
    throw error;
  }
};

export default api;