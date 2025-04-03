import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchProducts, fetchProduct, generateContent, completeProduct, generateProductImages } from '../services/api';
import { useAuth } from './AuthContext';

const ProductContext = createContext();

export function ProductProvider({ children }) {
  // State for product data
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  // Fetch products on component mount or when user changes
  useEffect(() => {
    const loadProducts = async () => {
      if (!user) return; // Don't fetch products if user is not logged in
      
      try {
        setIsLoading(true);
        setError(null);
        const data = await fetchProducts();
        setProducts(data);
      } catch (error) {
        console.error('Error fetching products:', error);
        if (error.response?.status === 401) {
          setError('Authentication error. Please log in again.');
        } else {
          setError('Failed to load products. Please try again later.');
        }
      } finally {
        setIsLoading(false);
      }
    };
    
    loadProducts();
  }, [user]);

  // Function to fetch a product by ID
  const fetchProductById = async (productId) => {
    try {
      setIsLoading(true);
      setError(null);
      const product = await fetchProduct(productId);
      return product;
    } catch (error) {
      console.error('Error fetching product:', error);
      if (error.response?.status === 401) {
        setError('Authentication error. Please log in again.');
      } else {
        setError('Failed to load product. Please try again later.');
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Function to save a completed product
  const saveProduct = async (productData) => {
    try {
      setIsLoading(true);
      setError(null);
      const savedProduct = await completeProduct(productData);
      
      // Update products list with the new product
      setProducts(prevProducts => [...prevProducts, savedProduct]);
      
      return savedProduct;
    } catch (error) {
      console.error('Error saving product:', error);
      if (error.response?.status === 401) {
        setError('Authentication error. Please log in again.');
      } else {
        setError('Failed to save product. Please try again.');
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Function to generate product images
  const generateImages = async (productId, imageOptions) => {
    try {
      setIsLoading(true);
      setError(null);
      const images = await generateProductImages(productId);
      return images;
    } catch (error) {
      console.error('Error generating images:', error);
      if (error.response?.status === 401) {
        setError('Authentication error. Please log in again.');
      } else {
        setError('Failed to generate images. Please try again.');
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    products,
    setProducts,
    selectedProduct,
    setSelectedProduct,
    generatedContent,
    setGeneratedContent,
    isLoading,
    setIsLoading,
    error,
    setError,
    saveProduct,
    generateImages,
    fetchProductById
  };

  return <ProductContext.Provider value={value}>{children}</ProductContext.Provider>;
}

export function useProduct() {
  const context = useContext(ProductContext);
  if (!context) {
    throw new Error('useProduct must be used within a ProductProvider');
  }
  return context;
} 