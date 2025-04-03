import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Divider,
  CircularProgress,
  Alert,
  TextField,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Save as SaveIcon,
  Edit as EditIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { useProduct } from '../context/ProductContext';

function ContentPreview() {
  const navigate = useNavigate();
  const { productId } = useParams();
  const { 
    selectedProduct, 
    generatedContent, 
    setGeneratedContent, 
    isLoading, 
    error,
    saveProduct,
    fetchProductById
  } = useProduct();
  
  const [editedContent, setEditedContent] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [loadingProduct, setLoadingProduct] = useState(false);
  const [productError, setProductError] = useState('');

  // Load product data if productId is provided (for existing products)
  useEffect(() => {
    const loadProduct = async () => {
      if (productId && !selectedProduct) {
        try {
          setLoadingProduct(true);
          setProductError('');
          const product = await fetchProductById(productId);
          if (product && product.content) {
            setEditedContent(product.content);
          }
        } catch (error) {
          setProductError(error.message || 'Failed to load product');
        } finally {
          setLoadingProduct(false);
        }
      }
    };

    loadProduct();
  }, [productId, selectedProduct, fetchProductById]);

  // Update edited content when generated content changes
  useEffect(() => {
    if (generatedContent) {
      setEditedContent(generatedContent);
    }
  }, [generatedContent]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setEditedContent(generatedContent || {});
    setIsEditing(false);
  };

  const handleSave = () => {
    setIsEditing(false);
  };

  const handleContentChange = (key, value) => {
    setEditedContent(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSaveToDatabase = async () => {
    try {
      setSaving(true);
      setSaveError('');
      setSaveSuccess(false);
      
      // Prepare product data with the edited content
      const productData = {
        ...selectedProduct,
        content: editedContent
      };
      
      // Save the product
      await saveProduct(productData);
      
      setSaveSuccess(true);
      
      // Navigate back to home after a short delay
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      setSaveError(error.message || 'Failed to save product. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleBack = () => {
    navigate('/generate');
  };

  // Show loading state while fetching product data
  if (loadingProduct) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  // Show error if product loading failed
  if (productError) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{productError}</Alert>
        <Button 
          variant="contained" 
          startIcon={<ArrowBackIcon />} 
          onClick={handleBack}
          sx={{ mt: 2 }}
        >
          Go Back
        </Button>
      </Container>
    );
  }

  // Show loading state while generating content
  if (isLoading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  // Show error if content generation failed
  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
        <Button 
          variant="contained" 
          startIcon={<ArrowBackIcon />} 
          onClick={handleBack}
          sx={{ mt: 2 }}
        >
          Go Back
        </Button>
      </Container>
    );
  }

  // Show empty state if no product or content is available
  if (!selectedProduct && !productId) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            No Product Selected
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Please generate a new product or select an existing one to preview.
          </Typography>
          <Button
            variant="contained"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ mt: 2 }}
          >
            Go to Generate
          </Button>
        </Paper>
      </Container>
    );
  }

  // Show warning if no content is available
  if (!generatedContent && !editedContent) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            No Content Available
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            This product doesn't have any generated content yet.
          </Typography>
          <Button
            variant="contained"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ mt: 2 }}
          >
            Go Back
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Content Preview
          </Typography>
          <Box>
            {isEditing ? (
              <>
                <Tooltip title="Save Changes">
                  <IconButton color="primary" onClick={handleSave}>
                    <CheckIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Cancel">
                  <IconButton color="error" onClick={handleCancel}>
                    <CloseIcon />
                  </IconButton>
                </Tooltip>
              </>
            ) : (
              <Tooltip title="Edit Content">
                <IconButton color="primary" onClick={handleEdit}>
                  <EditIcon />
                </IconButton>
              </Tooltip>
            )}
            <Tooltip title="Save to Database">
              <IconButton 
                color="success" 
                onClick={handleSaveToDatabase}
                disabled={saving}
              >
                <SaveIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {selectedProduct && (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Product Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">
                  <strong>Name:</strong> {selectedProduct.name}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">
                  <strong>Price:</strong> ${selectedProduct.price}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1">
                  <strong>Description:</strong> {selectedProduct.basic_description}
                </Typography>
              </Grid>
            </Grid>
          </Box>
        )}

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Generated Content
        </Typography>

        {saveError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {saveError}
          </Alert>
        )}

        {saveSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Product saved successfully! Redirecting to home page...
          </Alert>
        )}

        <Grid container spacing={3}>
          {Object.entries(editedContent).map(([key, value]) => (
            <Grid item xs={12} key={key}>
              <Typography variant="subtitle1" gutterBottom>
                {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
              </Typography>
              {isEditing ? (
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={value}
                  onChange={(e) => handleContentChange(key, e.target.value)}
                  variant="outlined"
                />
              ) : (
                <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                    {value}
                  </Typography>
                </Paper>
              )}
            </Grid>
          ))}
        </Grid>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
          >
            Back to Generate
          </Button>
          
          <Button
            variant="contained"
            color="primary"
            onClick={handleSaveToDatabase}
            disabled={saving}
            startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
          >
            {saving ? 'Saving...' : 'Save Product'}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default ContentPreview; 