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
  const { selectedProduct, setGeneratedContent, setSelectedProduct } = useProduct();
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

  const [productName, setProductName] = useState('');
  const [generatedImage, setGeneratedImage] = useState(null);
  const [tone, setTone] = useState('professional');
  const [length, setLength] = useState('medium');
  const [audience, setAudience] = useState('general');

  const handlePreviewClick = () => {
    if (selectedProduct && selectedProduct.id) {
      navigate(`/preview/${selectedProduct.id}`);
    } else {
      console.error('No product selected or product ID is missing.');
    }
  };

  const toneOptions = [
    { value: 'professional', label: 'Professional' },
    { value: 'casual', label: 'Casual' },
    { value: 'enthusiastic', label: 'Enthusiastic' },
    { value: 'technical', label: 'Technical' },
    { value: 'friendly', label: 'Friendly' },
    { value: 'luxury', label: 'Luxury' }
    ];
    
    // Available length options
    const lengthOptions = [
    { value: 'short', label: 'Short' },
    { value: 'medium', label: 'Medium' },
    { value: 'long', label: 'Long' }
    ];
    
    // Available audience options
    const audienceOptions = [
    { value: 'general', label: 'General' },
    { value: 'technical', label: 'Technical' },
    { value: 'beginners', label: 'Beginners' },
    { value: 'experts', label: 'Experts' },
    { value: 'business', label: 'Business' },
    { value: 'youth', label: 'Youth' }
    ];



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

      const payload = {
        ...formData,
        descriptionOptions: {
          tone,
          length,
          audience,
        }
      };

      // First create the product
      const createdProduct = await createProduct(formData);

      // Set the selected product in context
      setSelectedProduct(createdProduct);

      // Generate content with form data using the created product's ID
      const content = await generateSectionContent(createdProduct.id, 'product', payload);
      setGeneratedContent(content);
      setGenerationComplete(true);
    } catch (error) {
      setError(error.message || 'Failed to generate content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '80vh',
        textAlign: 'center',

        borderRadius: 2,
        boxShadow: 3,

        p: 4,
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

            boxShadow: 6, // Enhance shadow for depth
            borderRadius: 4, // Rounded corners for a modern look

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
            {/* Product Details */}
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
  
            {/* Features, Materials, Colors, Tags */}
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
            </Grid>

            <Divider sx={{ my: 4 }} />

            {/* Generate Product Description Section */}
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h5" component="h2" gutterBottom sx={{ mt: 3 }}>
                  Generate Product Description
                </Typography>
              </Grid>
  
            {/* Description Options */}
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={4}>
                <FormControl fullWidth margin="normal" sx={{ minWidth: 200 }}>
                  <InputLabel>Tone</InputLabel>
                  <Select value={tone} onChange={(e) => setTone(e.target.value)}>
                    {toneOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <FormControl fullWidth margin="normal" sx={{ minWidth: 200 }}>
                  <InputLabel>Length</InputLabel>
                  <Select value={length} onChange={(e) => setLength(e.target.value)}>
                    {lengthOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <FormControl fullWidth margin="normal" sx={{ minWidth: 200 }}>
                  <InputLabel>Target Audience</InputLabel>
                  <Select value={audience} onChange={(e) => setAudience(e.target.value)}>
                    {audienceOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            </Grid>
  
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
          onClick={handlePreviewClick}
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
