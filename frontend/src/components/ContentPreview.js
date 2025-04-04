import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
} from '@mui/material';
import { fetchProduct } from '../services/api';

function ContentPreview() {
  const { productId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [product, setProduct] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    const loadProduct = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await fetchProduct(productId);
        setProduct(data);
      } catch (error) {
        console.error('Error loading product:', error);
        setError(error.message || 'Failed to load product');
      } finally {
        setLoading(false);
      }
    };

    if (productId) {
      loadProduct();
    }
  }, [productId]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!product) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="warning">Product not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{
      display: 'flex',
      justifyContent: 'center',
      minHeight: '100vh', // Full viewport height
      width: '95vw', // Full viewport width
      padding: 2,
      transform: 'translateX(-2.0%)'
    }}>
      <Paper sx={{ p: 4, flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom>
          {product.name}
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange}>
            <Tab label="Description" />
            <Tab label="Features" />
            <Tab label="Benefits" />
            <Tab label="Specifications" />
          </Tabs>
        </Box>

        {activeTab === 0 && (
          <Box>
            <Typography variant="h6" gutterBottom>Product Description</Typography>
            <Typography paragraph>{product.description || product.basic_description}</Typography>
          </Box>
        )}

        {activeTab === 1 && (
          <Box>
            <Typography variant="h6" gutterBottom>Features</Typography>
            {product.features && product.features.length > 0 ? (
              <ul>
                {product.features.map((feature, index) => (
                  <li key={index}>
                    <Typography>{feature}</Typography>
                  </li>
                ))}
              </ul>
            ) : (
              <Typography color="text.secondary">No features available</Typography>
            )}
          </Box>
        )}

        {activeTab === 2 && (
          <Box>
            <Typography variant="h6" gutterBottom>Benefits</Typography>
            <Typography paragraph>{product.benefits || 'No benefits available'}</Typography>
          </Box>
        )}

        {activeTab === 3 && (
          <Box>
            <Typography variant="h6" gutterBottom>Specifications</Typography>
            <Typography paragraph>{product.specifications || 'No specifications available'}</Typography>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default ContentPreview;
