import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Button,
  Box,
  Card,
  CardContent,
  CardActions,
  CardMedia,
  Divider,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  AutoAwesome as GenerateIcon,
  Preview as PreviewIcon,
  Image as ImageIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { useProduct } from '../context/ProductContext';
import { fetchProducts } from '../services/api';

function Home() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { products, setProducts, isLoading, error } = useProduct();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        setLoading(true);
        const data = await fetchProducts();
        setProducts(data);
      } catch (error) {
        console.error('Error loading products:', error);
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, [setProducts]);

  const handleGenerateClick = () => {
    navigate('/generate');
  };

  const handlePreviewClick = (productId) => {
    navigate(`/preview/${productId}`);
  };

  const handleImageClick = (productId) => {
    navigate(`/images/${productId}`);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Your Products
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<GenerateIcon />}
          onClick={handleGenerateClick}
        >
          Generate New Product
        </Button>
      </Box>

      <Divider sx={{ mb: 4 }} />

      {loading || isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ my: 2 }}>
          {error}
        </Alert>
      ) : !Array.isArray(products) || products.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            You haven't generated any products yet
          </Typography>
          <Button
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={handleGenerateClick}
            sx={{ mt: 2 }}
          >
            Create Your First Product
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={4}>
          {products.map((product) => (
            <Grid item xs={12} sm={6} md={4} key={product.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                {product.image_url && (
                  <CardMedia
                    component="img"
                    height="200"
                    image={product.image_url}
                    alt={product.name}
                  />
                )}
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="h3">
                    {product.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {product.basic_description}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Category: {product.category}
                  </Typography>
                  {product.subcategory && (
                    <Typography variant="body2" color="text.secondary">
                      Subcategory: {product.subcategory}
                    </Typography>
                  )}
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    startIcon={<PreviewIcon />}
                    onClick={() => handlePreviewClick(product.id)}
                  >
                    Preview
                  </Button>
                  <Button 
                    size="small" 
                    startIcon={<ImageIcon />}
                    onClick={() => handleImageClick(product.id)}
                  >
                    Images
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}

export default Home; 