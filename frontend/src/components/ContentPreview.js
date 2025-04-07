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
  Card,
  CardMedia,
  TextField,
  Button
} from '@mui/material';
import { fetchProduct, updateProduct } from '../services/api';

function ContentPreview() {

  const { productId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [product, setProduct] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [activeSubTab, setActiveSubTab] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState('');

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
    setIsEditing(false); 
    setEditedContent('');
  };

  const handleSubTabChange = (event, newValue) => {
    setActiveSubTab(newValue);
    setIsEditing(false); // Reset editing state
    setEditedContent(''); // Clear edited content
  };

  const handleEditClick = (currentContent) => {
    setIsEditing(true);
    setEditedContent(currentContent || '');
  };

  const handleSaveClick = async (field) => {
    try {
      let updatedFieldContent = editedContent;
      if (["materials", "colors", "tags"].includes(field)) {
        updatedFieldContent = editedContent
          .split("\n") // Split by newline
          .map((item) => item.trim()) // Trim whitespace
          .filter((item) => item); // Remove empty items
      }
      
      let updatedProduct = { ...product };
      
      if (field.split('.').length === 2) {
        const email_copy = { ...product.marketing_copy.email, [field.split('.')[1]]: String(updatedFieldContent) };
        updatedProduct = { ...product, marketing_copy: { ...product.marketing_copy, email: email_copy } };
      }

      if (field.split('.').length === 3) {
        const social_media_copy = {
            ...product.marketing_copy.social_media,
            [field.split('.')[2]]: updatedFieldContent,
        };

        updatedProduct = {
            ...product,
            marketing_copy: {
                ...product.marketing_copy,
                social_media: social_media_copy,
            },
        };
      }

      if (field.split('.').length === 1) {
        updatedProduct = { ...product, [field]: updatedFieldContent };
      }
      await updateProduct(productId, updatedProduct); // Save to database
      setProduct(updatedProduct); // Update local state
      setIsEditing(false);
    } catch (error) {
      console.error('Error saving product:', error);
      setError('Failed to save changes');
    }
  };

  const handleGenerateClick = async (field) => {
    try {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/products/${productId}/generate-field?field=${field}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        throw new Error('Failed to generate content');
      }
  
      const data = await response.json();
      setEditedContent(data.generated_content); // Set the generated content for editing
      setIsEditing(true); // Enable editing mode
    } catch (error) {
      console.error('Error generating content:', error);
      setError('Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  const handleRevertClick = () => {
    setIsEditing(false); // Exit editing mode
    setEditedContent(''); // Clear the edited content
  };

  const marketingTabs = ['Email', 'Instagram', 'Facebook', 'LinkedIn', 'Twitter'];

  if (!product) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '80vh',
          textAlign: 'center',
          backgroundColor: '#f9f9f9',
          borderRadius: 2,
          boxShadow: 3,
          p: 4,
        }}
      >
        <Typography variant="h5" color="text.secondary" gutterBottom>
          Oops! No product data found.
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          It seems like no product data is available. Please generate content first or go back to the form to create a new product.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={() => navigate('/')}
          sx={{ textTransform: 'none', px: 4 }}
        >
          Return to Home Page
        </Button>
      </Box>
    );
  }

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
      width: '80vw', // Full viewport width
      padding: 2,
      transform: 'translateX(-2.0%)'
    }}>
      <Paper sx={{ p: 4, flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom>
          {product.name}
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          {/* Main Tabs */}
          <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable">
            <Tab label="Description" />
            <Tab label="Features" />
            <Tab label="Materials" />
            <Tab label="Tags" />
            <Tab label="Image" />
            <Tab label="SEO Data" />
            <Tab label="Marketing Copy" />
          </Tabs>
        </Box>

        {activeTab === 0 && (
        <Box>
          <Typography variant="h6" gutterBottom>Product Description</Typography>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                label="Basic Description"
                value={product.basic_description}
                onChange={(e) => setProduct({ ...product, basic_description: e.target.value })}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Detailed Description"
                value={product.detailed_description}
                onChange={(e) => setProduct({ ...product, detailed_description: e.target.value })}
                sx={{ mb: 2 }}
              />
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleSaveClick(['basic_description', 'detailed_description'])}
                >
                  Save All
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={handleRevertClick}
                >
                  Revert
                </Button>
              </Box>
            </>
          ) : (
            <>
              <Typography paragraph>
                <strong>Basic Description:</strong> {product.basic_description || 'No basic description available.'}
              </Typography>
              <Typography paragraph>
                <strong>Detailed Description:</strong> {product.detailed_description || 'No detailed description available.'}
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button
                  variant="outlined"
                  onClick={() => setIsEditing(true)}
                >
                  Edit
                </Button>
              </Box>
            </>
          )}
        </Box>
      )}

        {activeTab === 1 && (
          <Box>
            <Typography variant="h6" gutterBottom>Features</Typography>
            {isEditing ? (
              <>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                />
                <Button variant="contained" color="primary" onClick={() => handleSaveClick('features')} sx={{ mt: 2 }}>
                  Save
                </Button>
              </>
            ) : (
              <>
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
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('features')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                  <Button variant="outlined" onClick={() => handleEditClick(product.features.join('\n'))}>
                    Edit
                  </Button>
                </Box>
              </>
            )}
          </Box>
        )}

        {activeTab === 2 && (
          <Box>
            <Typography variant="h6" gutterBottom>Materials</Typography>
            {isEditing ? (
              <>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                />
                <Button variant="contained" color="primary" onClick={() => handleSaveClick('materials')} sx={{ mt: 2 }}>
                  Save
                </Button>
              </>
            ) : (
              <>
                {product.materials && product.materials.length > 0 ? (
                  <ul>
                    {product.materials.map((material, index) => (
                      <li key={index}>
                        <Typography>{material}</Typography>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <Typography color="text.secondary">No materials available</Typography>
                )}
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('materials')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                  <Button variant="outlined" onClick={() => handleEditClick(product.materials.join('\n'))}>
                    Edit
                  </Button>
                </Box>
              </>
            )}
          </Box>
        )}

        {activeTab === 3 && (
          <Box>
            <Typography variant="h6" gutterBottom>Tags</Typography>
            {isEditing ? (
              <>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                />
                <Button variant="contained" color="primary" onClick={() => handleSaveClick('tags')} sx={{ mt: 2 }}>
                  Save
                </Button>
              </>
            ) : (
              <>
                {product.tags && product.tags.length > 0 ? (
                  <ul>
                    {product.tags.map((tag, index) => (
                      <li key={index}>
                        <Typography>{tag}</Typography>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <Typography color="text.secondary">No tags available</Typography>
                )}
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('tags')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                  <Button variant="outlined" onClick={() => handleEditClick(product.tags.join(', '))}>
                    Edit
                  </Button>
                </Box>
              </>
            )}
          </Box>
        )}

        {activeTab === 4 && (
          <Box>
            <Typography variant="h6" gutterBottom>Image</Typography>
            {isEditing ? (
              <>
                <TextField
                  fullWidth
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                />
                <Button variant="contained" color="primary" onClick={() => handleSaveClick('image_url')} sx={{ mt: 2 }}>
                  Save
                </Button>
              </>
            ) : (
              <>
                {product.image_url ? (
                  <Card>
                    <CardMedia
                      component="img"
                      height="1024"
                      image={product.image_url}
                      alt={product.name}
                    />
                  </Card>
                ) : (
                  <Typography color="text.secondary">No image available</Typography>
                )}
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('image_url')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                  <Button variant="outlined" onClick={() => handleEditClick(product.image_url)}>
                    Edit
                  </Button>
                </Box>
              </>
            )}
          </Box>
        )}

        {activeTab === 5 && (
          <Box>
            <Typography variant="h6" gutterBottom>SEO Data</Typography>
            {isEditing ? (
              <>
                <TextField
                  fullWidth
                  label="SEO Title"
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="SEO Description"
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
                />
                <Button variant="contained" color="primary" onClick={() => handleSaveClick('seo_data')} sx={{ mt: 2 }}>
                  Save
                </Button>
              </>
            ) : (
              <>
                <Typography>
                  <strong>Title:</strong> {product.seo_title || 'No SEO title available'}
                </Typography>
                <Typography>
                  <strong>Description:</strong> {product.seo_description || 'No SEO description available'}
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                  <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('seo_data')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                  <Button variant="outlined" onClick={() => handleEditClick(`${product.seo_title}\n${product.seo_description}`)}>
                    Edit
                  </Button>
                </Box>
              </>
            )}
          </Box>
        )}

{activeTab === 6 && (
  <Box>
    <Typography variant="h6" gutterBottom>Marketing Copy</Typography>
    <Tabs value={activeSubTab} onChange={handleSubTabChange} variant="scrollable">
      {marketingTabs.map((tab, index) => (
        <Tab key={index} label={tab} />
      ))}
    </Tabs>

    <Box mt={3}>
      {activeSubTab === 0 && (
        <>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={() => handleSaveClick('marketing_copy.email')} sx={{ mt: 2 }}>
                Save
              </Button>
            </>
          ) : (
            <>
              <Typography
               sx={{ whiteSpace: 'pre-line' }}
              >{product.marketing_copy.email || 'No email copy available'}</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('marketing_copy.email')} sx={{ ml: 2 }}>
                    Generate
                </Button>
                {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                <Button variant="outlined" onClick={() => handleEditClick(product.marketing_copy.email)}>
                  Edit
                </Button>
              </Box>
            </>
          )}
        </>
      )}
      {activeSubTab === 1 && (
        <>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={() => handleSaveClick('marketing_copy.social_media.instagram')} sx={{ mt: 2 }}>
                Save
              </Button>
            </>
          ) : (
            <>
              <Typography
               sx={{ whiteSpace: 'pre-line' }}
              >{product.marketing_copy.social_media.instagram || 'No Instagram copy available'}</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('marketing_copy.social_media.instagram')} sx={{ ml: 2 }}>
                    Generate
                </Button>
                {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                <Button variant="outlined" onClick={() => handleEditClick(product.marketing_copy.social_media.instagram)}>
                  Edit
                </Button>
              </Box>
            </>
          )}
        </>
      )}
      {activeSubTab === 2 && (
        <>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={() => handleSaveClick('marketing_copy.social_media.facebook')} sx={{ mt: 2 }}>
                Save
              </Button>
            </>
          ) : (
            <>
              <Typography
               sx={{ whiteSpace: 'pre-line' }}
              >{product.marketing_copy.social_media.facebook || 'No Facebook copy available'}</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('marketing_copy.social_media.facebook')} sx={{ ml: 2 }}>
                    Generate
                </Button>
                {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                <Button variant="outlined" onClick={() => handleEditClick(product.marketing_copy.social_media.facebook)}>
                  Edit
                </Button>
              </Box>
            </>
          )}
        </>
      )}
      {activeSubTab === 3 && (
        <>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={() => handleSaveClick('marketing_copy.social_media.linkedin')} sx={{ mt: 2 }}>
                Save
              </Button>
            </>
          ) : (
            <>
              <Typography
               sx={{ whiteSpace: 'pre-line' }}
              >{product.marketing_copy.social_media.linkedin || 'No LinkedIn copy available'}</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('marketing_copy.social_media.linkedin')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                <Button variant="outlined" onClick={() => handleEditClick(product.marketing_copy.social_media.linkedin)}>
                  Edit
                </Button>
              </Box>
            </>
          )}
        </>
      )}
      {activeSubTab === 4 && (
        <>
          {isEditing ? (
            <>
              <TextField
                fullWidth
                multiline
                rows={4}
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
              />
              <Button variant="contained" color="primary" onClick={() => handleSaveClick('marketing_copy.social_media.twitter')} sx={{ mt: 2 }}>
                Save
              </Button>
            </>
          ) : (
            <>
              <Typography
               sx={{ whiteSpace: 'pre-line' }}
              >{product.marketing_copy.social_media.twitter || 'No Tweet available'}</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button variant="contained" color="secondary" onClick={() => handleGenerateClick('marketing_copy.social_media.twitter')} sx={{ ml: 2 }}>
                    Generate
                  </Button>
                  {isEditing && (
                    <Button variant="outlined" color="error" onClick={handleRevertClick}>
                      Revert
                    </Button>
                  )}
                <Button variant="outlined" onClick={() => handleEditClick(product.marketing_copy.social_media.twitter)}>
                  Edit
                </Button>
              </Box>
            </>
          )}
        </>
      )}
        </Box>
      </Box>
    )}
</Paper>
</Container>
);
}

export default ContentPreview;
