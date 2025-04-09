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
    <Container maxWidth={false} sx={{ py: 4 }}>
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
        <Grid container spacing={3} sx={{ justifyContent: 'left' }}>
          {products.map((product) => (
            <Grid item xs={12} sm={6} md={2.4} lg={2.4} key={product.id}>
              {/* Each card takes up approximately one-fifth of the row */}
              <Card
                sx={{
                  height: '400px',
                  display: 'flex',
                  flexDirection: 'column',
                  maxWidth: '220px',
                  boxShadow: 3,
                  borderRadius: 2,
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'scale(1.05)',
                  },
                }}
              >
                {product.image_url ? (
                  <CardMedia
                    component="img"
                    height="200"
                    image={product.image_url}
                    alt={product.name}
                    sx={{
                      objectFit: 'cover',
                      borderBottom: '1px solid #e0e0e0',
                    }}
                  />
                ) : (
                  <Box
                    sx={{
                      height: '200px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: '#f5f5f5',
                      borderBottom: '1px solid #e0e0e0',
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      No Image Available
                    </Typography>
                  </Box>
                )}
                <CardContent
                  sx={{
                    flexGrow: 1,
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  <Typography gutterBottom variant="h6" component="h3">
                    {product.name}
                  </Typography>
                  <Box
                    sx={{
                      height: '50px', // Fixed height for description box
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                       // Ensures text truncation with ellipsis
                      mb: 1,
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      {product.basic_description || 'No description available.'}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Category: {product.category || 'N/A'}
                  </Typography>
                  {product.subcategory && (
                    <Typography variant="body2" color="text.secondary">
                      Subcategory: {product.subcategory}
                    </Typography>
                  )}
                </CardContent>
                <CardActions sx={{ justifyContent: 'center' }}>
                  <Button
                    size="small"
                    startIcon={<PreviewIcon />}
                    onClick={() => handlePreviewClick(product.id)}
                  >
                    Preview
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
