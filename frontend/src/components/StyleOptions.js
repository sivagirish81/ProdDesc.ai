import React from 'react';

const StyleOptions = ({ 
  styleOptions, 
  socialMediaPlatforms,
  imageStyleOptions = {},
  onStyleChange, 
  onSocialMediaChange,
  onImageStyleChange,
  showSocialMedia,
  showImageOptions
}) => {
  // Available tone options
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
  
  // Available image background options
  const backgroundOptions = [
    { value: 'white', label: 'White' },
    { value: 'studio', label: 'Studio' },
    { value: 'gradient', label: 'Gradient' },
    { value: 'contextual', label: 'Contextual' },
    { value: 'outdoor', label: 'Outdoor' },
    { value: 'minimalist', label: 'Minimalist' }
  ];
  
  // Available image lighting options
  const lightingOptions = [
    { value: 'studio', label: 'Studio' },
    { value: 'natural', label: 'Natural' },
    { value: 'dramatic', label: 'Dramatic' },
    { value: 'soft', label: 'Soft' },
    { value: 'bright', label: 'Bright' }
  ];
  
  // Available image angle options
  const angleOptions = [
    { value: 'front', label: 'Front' },
    { value: 'side', label: 'Side' },
    { value: 'top-down', label: 'Top-Down' },
    { value: 'three-quarter', label: 'Three-Quarter' },
    { value: '45-degree', label: '45-Degree' }
  ];
  
  // Handle style option changes
  const handleStyleChange = (e) => {
    const { name, value } = e.target;
    onStyleChange({
      ...styleOptions,
      [name]: value
    });
  };
  
  // Handle keywords change
  const handleKeywordsChange = (e) => {
    const keywords = e.target.value ? 
      e.target.value.split(',').map(keyword => keyword.trim()) : 
      [];
    
    onStyleChange({
      ...styleOptions,
      keywords
    });
  };
  
  // Handle social media platform changes
  const handleSocialMediaChange = (e) => {
    const { name, checked } = e.target;
    onSocialMediaChange({
      ...socialMediaPlatforms,
      [name]: checked
    });
  };
  
  // Handle image style option changes
  const handleImageStyleChange = (e) => {
    const { name, value } = e.target;
    onImageStyleChange({
      ...imageStyleOptions,
      [name]: value
    });
  };
  
  return (
    <div className="style-options-container">
      <h2>Style Options</h2>
      <p>Customize the style and tone of the generated content:</p>
      
      <div className="style-option">
        <label htmlFor="tone">Tone:</label>
        <select 
          id="tone" 
          name="tone" 
          value={styleOptions.tone} 
          onChange={handleStyleChange}
        >
          {toneOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      
      <div className="style-option">
        <label htmlFor="length">Length:</label>
        <select 
          id="length" 
          name="length" 
          value={styleOptions.length} 
          onChange={handleStyleChange}
        >
          {lengthOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      
      <div className="style-option">
        <label htmlFor="audience">Target Audience:</label>
        <select 
          id="audience" 
          name="audience" 
          value={styleOptions.audience} 
          onChange={handleStyleChange}
        >
          {audienceOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      
      <div className="style-option">
        <label htmlFor="keywords">Keywords (comma-separated):</label>
        <input
          type="text"
          id="keywords"
          value={styleOptions.keywords.join(', ')}
          onChange={handleKeywordsChange}
          placeholder="e.g., quality, innovative, affordable"
        />
      </div>
      
      {showSocialMedia && (
        <div className="social-media-options">
          <h3>Social Media Platforms</h3>
          <p>Select the platforms to generate content for:</p>
          
          <div className="platform-options">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="instagram"
                checked={socialMediaPlatforms.instagram}
                onChange={handleSocialMediaChange}
              />
              Instagram
            </label>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="facebook"
                checked={socialMediaPlatforms.facebook}
                onChange={handleSocialMediaChange}
              />
              Facebook
            </label>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="twitter"
                checked={socialMediaPlatforms.twitter}
                onChange={handleSocialMediaChange}
              />
              Twitter
            </label>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="linkedin"
                checked={socialMediaPlatforms.linkedin}
                onChange={handleSocialMediaChange}
              />
              LinkedIn
            </label>
          </div>
        </div>
      )}
      
      {showImageOptions && (
        <div className="image-style-options">
          <h3>Image Style Options</h3>
          <p>Customize the appearance of the generated product image:</p>
          
          <div className="style-option">
            <label htmlFor="background">Background:</label>
            <select 
              id="background" 
              name="background" 
              value={imageStyleOptions.background || 'white'} 
              onChange={handleImageStyleChange}
            >
              {backgroundOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div className="style-option">
            <label htmlFor="lighting">Lighting:</label>
            <select 
              id="lighting" 
              name="lighting" 
              value={imageStyleOptions.lighting || 'studio'} 
              onChange={handleImageStyleChange}
            >
              {lightingOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div className="style-option">
            <label htmlFor="angle">Angle:</label>
            <select 
              id="angle" 
              name="angle" 
              value={imageStyleOptions.angle || 'front'} 
              onChange={handleImageStyleChange}
            >
              {angleOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default StyleOptions;