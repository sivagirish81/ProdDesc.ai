import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { 
  fetchProducts, 
  fetchProduct, 
  createProduct, 
  updateProduct, 
  generateSectionContent,
  generateProductImages 
} from '../services/api';

const ProductContext = createContext();

export const useProduct = () => {
  return useContext(ProductContext);
};

export const ProductProvider = ({ children }) => {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const loadProducts = async () => {
      if (user) {
        try {
          setIsLoading(true);
          setError('');
          const data = await fetchProducts();
          setProducts(data);
        } catch (error) {
          setError(error.message || 'Failed to load products');
          if (error.response?.status === 401) {
            // Handle authentication error
            setProducts([]);
          }
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadProducts();
  }, [user]);

  const fetchProductById = async (id) => {
    try {
      setIsLoading(true);
      setError('');
      const data = await fetchProduct(id);
      return data;
    } catch (error) {
      setError(error.message || 'Failed to fetch product');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const saveProduct = async (productData) => {
    try {
      setIsLoading(true);
      setError('');
      let savedProduct;
      if (productData.id) {
        savedProduct = await updateProduct(productData.id, productData);
      } else {
        savedProduct = await createProduct(productData);
      }
      return savedProduct;
    } catch (error) {
      setError(error.message || 'Failed to save product');
      if (error.response?.status === 401) {
        // Handle authentication error
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const generateImages = async (productId, options) => {
    try {
      setIsLoading(true);
      setError('');
      const data = await generateProductImages(productId, options);
      return data;
    } catch (error) {
      setError(error.message || 'Failed to generate images');
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
    error,
    fetchProductById,
    saveProduct,
    generateImages
  };

  return (
    <ProductContext.Provider value={value}>
      {children}
    </ProductContext.Provider>
  );
}; 