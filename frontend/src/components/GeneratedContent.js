import React, { useState } from 'react';

const GeneratedContent = ({ content, contentTypes, isLoading }) => {
  // State for the active tab
  const [activeTab, setActiveTab] = useState(contentTypes[0] || 'product_description');
  
  // Handle tab click
  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };
  
  // Check if we have content for a specific type
  const hasContent = (type) => {
    return content && content[type];
  };
  
  // Render content for a specific type
  const renderContent = (type) => {
    if (!content || !content[type]) {
      return null;
    }
    
    switch (type) {
      case 'product_description':
        return (
          <div className="description-content">
            <h3>Product Description</h3>
            <div className="content-box">
              <p>{content.product_description.detailed_description}</p>
            </div>
            <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.product_description.detailed_description)}>
              Copy to Clipboard
            </button>
          </div>
        );
        
      case 'seo':
        return (
          <div className="seo-content">
            <h3>SEO Content</h3>
            
            <div className="content-section">
              <h4>Title Tag</h4>
              <div className="content-box">
                <p>{content.seo.title}</p>
              </div>
              <p className="character-count">
                {content.seo.title.length} characters
                {content.seo.title.length > 60 ? 
                  content.seo.title.length > 70 ? 
                    " (Too long!)" : 
                    " (Near limit)" : 
                  ""}
              </p>
              <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.seo.title)}>
                Copy Title
              </button>
            </div>
            
            <div className="content-section">
              <h4>Meta Description</h4>
              <div className="content-box">
                <p>{content.seo.description}</p>
              </div>
              <p className="character-count">
                {content.seo.description.length} characters
                {content.seo.description.length > 150 ? 
                  content.seo.description.length > 160 ? 
                    " (Too long!)" : 
                    " (Near limit)" : 
                  ""}
              </p>
              <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.seo.description)}>
                Copy Description
              </button>
            </div>
          </div>
        );
        
      case 'marketing_email':
        return (
          <div className="email-content">
            <h3>Marketing Email</h3>
            
            <div className="content-section">
              <h4>Subject Line</h4>
              <div className="content-box">
                <p>{content.marketing_email.subject}</p>
              </div>
              <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.marketing_email.subject)}>
                Copy Subject
              </button>
            </div>
            
            <div className="content-section">
              <h4>Email Body</h4>
              <div className="content-box email-body">
                {content.marketing_email.body.split('\n').map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
              <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.marketing_email.body)}>
                Copy Body
              </button>
            </div>
            
            <button className="copy-btn copy-all" onClick={() => navigator.clipboard.writeText(
              `Subject: ${content.marketing_email.subject}\n\n${content.marketing_email.body}`
            )}>
              Copy Complete Email
            </button>
          </div>
        );
        
      case 'social_media':
        return (
          <div className="social-media-content">
            <h3>Social Media Content</h3>
            
            {content.social_media.instagram && (
              <div className="content-section">
                <h4>Instagram</h4>
                <div className="content-box">
                  <p>{content.social_media.instagram}</p>
                </div>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.social_media.instagram)}>
                  Copy Instagram
                </button>
              </div>
            )}
            
            {content.social_media.facebook && (
              <div className="content-section">
                <h4>Facebook</h4>
                <div className="content-box">
                  <p>{content.social_media.facebook}</p>
                </div>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.social_media.facebook)}>
                  Copy Facebook
                </button>
              </div>
            )}
            
            {content.social_media.twitter && (
              <div className="content-section">
                <h4>Twitter</h4>
                <div className="content-box">
                  <p>{content.social_media.twitter}</p>
                </div>
                <p className="character-count">
                  {content.social_media.twitter.length} characters
                  {content.social_media.twitter.length > 260 ? 
                    content.social_media.twitter.length > 280 ? 
                      " (Too long!)" : 
                      " (Near limit)" : 
                    ""}
                </p>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.social_media.twitter)}>
                  Copy Twitter
                </button>
              </div>
            )}
            
            {content.social_media.linkedin && (
              <div className="content-section">
                <h4>LinkedIn</h4>
                <div className="content-box">
                  <p>{content.social_media.linkedin}</p>
                </div>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.social_media.linkedin)}>
                  Copy LinkedIn
                </button>
              </div>
            )}
          </div>
        );
        
      case 'missing_fields':
        return (
          <div className="missing-fields-content">
            <h3>Generated Missing Fields</h3>
            
            {Object.entries(content.missing_fields).map(([field, value]) => {
              if (Array.isArray(value)) {
                return (
                  <div key={field} className="content-section">
                    <h4>{field.charAt(0).toUpperCase() + field.slice(1)}</h4>
                    <div className="content-box">
                      <ul>
                        {value.map((item, index) => (
                          <li key={index}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                );
              } else if (typeof value === 'object') {
                return (
                  <div key={field} className="content-section">
                    <h4>{field.charAt(0).toUpperCase() + field.slice(1)}</h4>
                    <div className="content-box">
                      <pre>{JSON.stringify(value, null, 2)}</pre>
                    </div>
                  </div>
                );
              } else {
                return (
                  <div key={field} className="content-section">
                    <h4>{field.charAt(0).toUpperCase() + field.slice(1)}</h4>
                    <div className="content-box">
                      <p>{value}</p>
                    </div>
                  </div>
                );
              }
            })}
          </div>
        );
        
      case 'product_image':
        return (
          <div className="product-image-content">
            <h3>Generated Product Image</h3>
            
            <div className="content-section">
              <h4>Image</h4>
              <div className="content-box image-container">
                <img 
                  src={content.product_image.image_url} 
                  alt="Generated product" 
                  className="generated-image" 
                />
              </div>
              <div className="content-section">
                <h4>Prompt Used</h4>
                <div className="content-box">
                  <p>{content.product_image.prompt}</p>
                </div>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(content.product_image.prompt)}>
                  Copy Prompt
                </button>
              </div>
              <a 
                href={content.product_image.image_url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="download-link"
              >
                Open Full Size Image
              </a>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="generated-content-container">
      <h2>Generated Content</h2>
      
      {isLoading ? (
        <div className="loading-message">
          <p>Generating content...</p>
          <div className="loading-spinner"></div>
        </div>
      ) : content ? (
        <div className="content-tabs-container">
          <div className="content-tabs">
            {contentTypes.map(type => (
              <button
                key={type}
                className={`tab-button ${activeTab === type ? 'active' : ''} ${hasContent(type) ? 'has-content' : 'no-content'}`}
                onClick={() => handleTabClick(type)}
              >
                {type === 'product_description' && 'Product Description'}
                {type === 'seo' && 'SEO Content'}
                {type === 'marketing_email' && 'Marketing Email'}
                {type === 'social_media' && 'Social Media'}
                {type === 'missing_fields' && 'Missing Fields'}
              </button>
            ))}
          </div>
          
          <div className="content-panel">
            {hasContent(activeTab) ? (
              renderContent(activeTab)
            ) : (
              <div className="no-content-message">
                <p>No content generated for this type yet. Click "Generate Content" to create content.</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="no-content-message">
          <p>Select a product or create a custom one, then click "Generate Content" to get started.</p>
        </div>
      )}
    </div>
  );
};

export default GeneratedContent;