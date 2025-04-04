import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  Grid,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip,
  useTheme,
  useMediaQuery,
  Tabs,
  Tab,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
} from '@mui/material';
import {
  Save as SaveIcon,
  Edit as EditIcon,
  ArrowBack as ArrowBackIcon,
  Description as DescriptionIcon,
  Category as CategoryIcon,
  Build as BuildIcon,
  Info as InfoIcon,
  AutoAwesome as GenerateIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useProduct } from '../context/ProductContext';
import { useAuth } from '../context/AuthContext';
import { fetchProductById, updateProduct, deleteProduct, generateSectionContent, completeProduct } from '../services/api';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`product-tabpanel-${index}`}
      aria-labelledby={`product-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

function Preview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const loadProduct = async () => {
      if (!user) {
        navigate('/login');
        return;
      }

      try {
        setLoading(true);
        const data = await fetchProductById(id);
        setProduct(data);
      } catch (err) {
        console.error('Error loading product:', err);
        setError('Failed to load product details');
      } finally {
        setLoading(false);
      }
    };

    loadProduct();
  }, [id, user, navigate]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleFieldChange = (field, value) => {
    setProduct(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      const updatedProduct = await updateProduct(id, product);
      setProduct(updatedProduct);
      setSnackbar({
        open: true,
        message: 'Product updated successfully',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to update product',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateContent = async (section) => {
    try {
      setGenerating(true);
      const updatedProduct = await generateSectionContent(id, section);
      setProduct(updatedProduct);
      setSnackbar({
        open: true,
        message: 'Content generated successfully',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to generate content',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleCompleteProduct = async () => {
    try {
      setGenerating(true);
      const updatedProduct = await completeProduct(id);
      setProduct(updatedProduct);
      setSnackbar({
        open: true,
        message: 'Product completed successfully',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to complete product',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleDelete = async () => {
    try {
      setLoading(true);
      await deleteProduct(id);
      navigate('/');
      setSnackbar({
        open: true,
        message: 'Product deleted successfully',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to delete product',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setLoading(false);
      setDeleteDialogOpen(false);
    }
  };

  if (loading && !product) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (!product) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Alert severity="warning">Product not found</Alert>
      </Box>
    );
  }

  const sections = [
    { label: 'Basic Info', fields: ['name', 'category', 'subcategory', 'basic_description'] },
    { label: 'Detailed Description', fields: ['detailed_description'] },
    { label: 'Technical Specs', fields: ['technical_specifications'] },
    { label: 'Key Features', fields: ['key_features'] },
    { label: 'Usage Instructions', fields: ['usage_instructions'] }
  ];

  return (
    <Container>
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Box display="flex" alignItems="center" gap={2}>
            <IconButton onClick={() => navigate('/')}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h4">{product.name}</Typography>
          </Box>
          <Box>
            <Button
              variant="contained"
              color="primary"
              startIcon={<SaveIcon />}
              onClick={handleSave}
              disabled={loading}
              sx={{ mr: 1 }}
            >
              Save
            </Button>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<RefreshIcon />}
              onClick={handleCompleteProduct}
              disabled={generating}
              sx={{ mr: 1 }}
            >
              Complete All
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => setDeleteDialogOpen(true)}
              disabled={loading}
            >
              Delete
            </Button>
          </Box>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable">
            {sections.map((section, index) => (
              <Tab key={index} label={section.label} />
            ))}
          </Tabs>
        </Paper>

        <Paper sx={{ p: 3 }}>
          <Grid container spacing={3}>
            {sections[activeTab].fields.map((field) => (
              <Grid item xs={12} key={field}>
                <Box display="flex" alignItems="flex-start" gap={2}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    label={field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    value={product[field] || ''}
                    onChange={(e) => handleFieldChange(field, e.target.value)}
                    variant="outlined"
                  />
                  <Button
                    variant="outlined"
                    onClick={() => handleGenerateContent(field)}
                    disabled={generating}
                    sx={{ minWidth: '120px' }}
                  >
                    {generating ? <CircularProgress size={24} /> : 'Generate'}
                  </Button>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Paper>

        <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
          <DialogTitle>Delete Product</DialogTitle>
          <DialogContent>
            <Typography>Are you sure you want to delete this product? This action cannot be undone.</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleDelete} color="error" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : 'Delete'}
            </Button>
          </DialogActions>
        </Dialog>

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          <Alert
            onClose={() => setSnackbar({ ...snackbar, open: false })}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default Preview; 