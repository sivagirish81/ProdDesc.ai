import React from 'react';

const ContentType = ({ selectedContentTypes, onContentTypeChange }) => {
  // Available content types
  const contentTypes = [
    {
      id: 'product_description',
      name: 'Product Description',
      description: 'Detailed and compelling product description'
    },
    {
      id: 'seo',
      name: 'SEO Content',
      description: 'SEO-optimized title and meta description'
    },
    {
      id: 'marketing_email',
      name: 'Marketing Email',
      description: 'Email marketing copy with subject line and body'
    },
    {
      id: 'social_media',
      name: 'Social Media',
      description: 'Posts for various social media platforms'
    },
    {
      id: 'missing_fields',
      name: 'Missing Fields',
      description: 'Generate any missing product information'
    },
    {
      id: 'product_image',
      name: 'Product Image',
      description: 'Generate product image based on attributes'
    }
  ];
  
  // Handle content type checkbox change
  const handleContentTypeChange = (e) => {
    const { value, checked } = e.target;
    
    if (checked) {
      // Add to selected types
      onContentTypeChange([...selectedContentTypes, value]);
    } else {
      // Remove from selected types
      onContentTypeChange(selectedContentTypes.filter(type => type !== value));
    }
  };
  
  return (
    <div className="content-type-container">
      <h2>Content Type</h2>
      <p>Select the type of content you want to generate:</p>
      
      <div className="content-type-options">
        {contentTypes.map(type => (
          <div key={type.id} className="content-type-option">
            <label className="checkbox-label">
              <input
                type="checkbox"
                value={type.id}
                checked={selectedContentTypes.includes(type.id)}
                onChange={handleContentTypeChange}
              />
              <span className="content-type-name">{type.name}</span>
            </label>
            <p className="content-type-description">{type.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContentType;