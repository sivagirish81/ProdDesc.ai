import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Card,
  CardMedia,
  CardContent,
  CardActions,
} from '@mui/material';
import axios from 'axios';

const imageStyles = [
  'product_photo',
  'lifestyle',
  'studio',
  'minimal',
  'e-commerce',
];

const imageSizes = [
  '512x512',
  '1024x1024',
  '1024x1792',
  '1792x1024',
];

function ImageGeneration() {
  const [prompt, setPrompt] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('product_photo');
  const [selectedSize, setSelectedSize] = useState('1024x1024');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImages, setGeneratedImages] = useState([]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/generate-image', {
        prompt,
        style: selectedStyle,
        size: selectedSize,
      });

      setGeneratedImages(prev => [...prev, response.data.image_url]);
    } catch (error) {
      console.error('Error generating image:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = (imageUrl) => {
    window.open(imageUrl, '_blank');
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Generate Product Images
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              label="Image Generation Prompt"
              placeholder="Describe the product image you want to generate..."
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Image Style</InputLabel>
              <Select
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                label="Image Style"
              >
                {imageStyles.map((style) => (
                  <MenuItem key={style} value={style}>
                    {style.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Image Size</InputLabel>
              <Select
                value={selectedSize}
                onChange={(e) => setSelectedSize(e.target.value)}
                label="Image Size"
              >
                {imageSizes.map((size) => (
                  <MenuItem key={size} value={size}>
                    {size}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleGenerate}
              disabled={isLoading || !prompt.trim()}
              startIcon={isLoading ? <CircularProgress size={20} /> : null}
            >
              {isLoading ? 'Generating...' : 'Generate Image'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {generatedImages.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Generated Images
          </Typography>
          <Grid container spacing={3}>
            {generatedImages.map((imageUrl, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card>
                  <CardMedia
                    component="img"
                    height="300"
                    image={imageUrl}
                    alt={`Generated product image ${index + 1}`}
                  />
                  <CardContent>
                    <Typography variant="body2" color="text.secondary">
                      Style: {selectedStyle}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Size: {selectedSize}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => handleDownload(imageUrl)}
                    >
                      Download
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}
    </Box>
  );
}

export default ImageGeneration; 