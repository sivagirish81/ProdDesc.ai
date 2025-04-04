import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material';
import { useProduct } from '../context/ProductContext';
import { createProduct, generateSectionContent } from '../services/api';

function ProductForm() {
  const navigate = useNavigate();
  const { setGeneratedContent, setSelectedProduct } = useProduct();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [generationComplete, setGenerationComplete] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    brand: '',
    basic_description: '',
    category: '',
    subcategory: '',
    features: [],
    materials: [],
    colors: [],
    tags: [],
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleArrayChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value.split(',').map((item) => item.trim()),
    }));
  };

  const handleGenerate = async () => {
    try {
      setLoading(true);
      setError('');
      setGenerationComplete(false);

      // First create the product
      const createdProduct = await createProduct(formData);

      // Set the selected product in context
      setSelectedProduct(createdProduct);

      // Generate content with form data using the created product's ID
      const content = await generateSectionContent(createdProduct.id, 'product', formData);
      setGeneratedContent(content);
      setGenerationComplete(true);
    } catch (error) {
      setError(error.message || 'Failed to generate content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = () => {
    navigate('/preview');
  };

  return (
    <Box
  sx={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh', // Full viewport height
    width: '100vw', // Full viewport width
    backgroundColor: '#f0f4f8', // Light background for aesthetics
    padding: 2, // Add padding around the box
  }}
>
  <Container
    maxWidth="lg"
    sx={{
      py: 4,
      flexGrow: 1,
      display: 'flex',

      transform: 'translateX(-5%)', // Shift container slightly to the left
    }}
  >
    <Paper
      sx={{
        p: 4,
        display: 'flex',
        flexDirection: 'column',
        width: '100%', // Occupy full width of the container
        maxWidth: 900, // Optional max width for better readability
        boxShadow: 6, // Enhance shadow for depth
        borderRadius: 4, // Rounded corners for a modern look
        backgroundColor: '#ffffff', // White background for contrast
      }}
    >
      <Typography variant="h4" component="h1" gutterBottom>
        Generate Product Content
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Product Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            margin="normal"
            required
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            margin="normal"
            required
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Brand"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            margin="normal"
            required
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <FormControl fullWidth margin="normal" sx={{ minWidth: 200 }}>
            <InputLabel>Category</InputLabel>
            <Select
              name="category"
              value={formData.category}
              onChange={handleChange}
              label="Category"
              required
            >
              <MenuItem value="electronics">Electronics</MenuItem>
              <MenuItem value="clothing">Clothing</MenuItem>
              <MenuItem value="home">Home & Kitchen</MenuItem>
              <MenuItem value="beauty">Beauty & Personal Care</MenuItem>
              <MenuItem value="sports">Sports & Outdoors</MenuItem>
              <MenuItem value="toys">Toys & Games</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Features (comma-separated)"
            value={formData.features.join(', ')}
            onChange={(e) => handleArrayChange('features', e.target.value)}
            margin="normal"
            helperText="Enter features separated by commas"
          />
        </Grid>
        {/* <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Subcategory"
            name="subcategory"
            value={formData.subcategory}
            onChange={handleChange}
            margin="normal"
          />
        </Grid> */}
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Basic Description"
            name="basic_description"
            value={formData.basic_description}
            onChange={handleChange}
            margin="normal"
            multiline
            rows={3}
            required
          />
        </Grid>
        {/* <Grid item xs={12}>
          <TextField
            fullWidth
            label="Features (comma-separated)"
            value={formData.features.join(', ')}
            onChange={(e) => handleArrayChange('features', e.target.value)}
            margin="normal"
            helperText="Enter features separated by commas"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Materials (comma-separated)"
            value={formData.materials.join(', ')}
            onChange={(e) => handleArrayChange('materials', e.target.value)}
            margin="normal"
            helperText="Enter materials separated by commas"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Colors (comma-separated)"
            value={formData.colors.join(', ')}
            onChange={(e) => handleArrayChange('colors', e.target.value)}
            margin="normal"
            helperText="Enter colors separated by commas"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Tags (comma-separated)"
            value={formData.tags.join(', ')}
            onChange={(e) => handleArrayChange('tags', e.target.value)}
            margin="normal"
            helperText="Enter tags separated by commas"
          />
        </Grid> */}
      </Grid>

      <Divider sx={{ my: 4 }} />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerate}
          disabled={loading}
          size="large"
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Generate Content'}
        </Button>

        <Button
          variant="outlined"
          color="secondary"
          onClick={handlePreview}
          disabled={!generationComplete || loading}
          size="large"
          fullWidth
        >
          Preview Content
        </Button>
      </Box>
    </Paper>
  </Container>
</Box>


  );
}

export default ProductForm;
