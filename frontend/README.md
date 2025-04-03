# AI-Powered Product Description Generator - Frontend

This is the frontend component of the AI-Powered Product Description Generator take-home assignment. It provides a React interface that allows users to generate compelling, SEO-optimized product descriptions, marketing copy, and product images based on basic product information.

## Project Structure

```
frontend/
│
├── public/
│   └── index.html
│
├── src/
│   ├── App.js           # Main application component
│   ├── index.js         # Entry point
│   ├── components/
│   │   ├── ProductForm.js   # Form for product data input (implement this)
│   │   ├── ContentType.js   # Content type selector (implement this)
│   │   ├── GeneratedContent.js  # Display for generated content (implement this)
│   │   └── StyleOptions.js  # Style and tone configuration (implement this)
│   │
│   ├── services/
│   │   └── api.js       # API client for backend communication
│   │
│   └── styles/
│       └── App.css      # Styling
│
├── package.json         # NPM dependencies
└── README.md            # This file
```

## Environment Setup

The frontend uses environment variables to manage configuration across different environments. Here's how to set it up:

### Environment Files

- `.env` - Base environment variables (committed to git)
- `.env.development` - Development environment variables (committed to git)
- `.env.production` - Production environment variables (committed to git)
- `.env.local` - Local overrides (not committed to git)

### Available Environment Variables

- `REACT_APP_API_URL` - The base URL for the API
  - Development: `http://localhost:8000`
  - Production: `https://api.proddesc.ai`

### Usage

1. For local development:
   ```bash
   npm start
   ```

2. For production build:
   ```bash
   npm run build
   ```

3. To override environment variables locally, create a `.env.local` file:
   ```
   REACT_APP_API_URL=http://your-local-api-url
   ```

### Best Practices

1. Never commit sensitive information in environment files
2. Use `.env.local` for local development overrides
3. Keep `.env.production` updated with production values
4. All environment variables must be prefixed with `REACT_APP_` to be accessible in the application

## Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Test the application
npm test
```

## Implementation Tasks

As part of this assignment, you need to implement the following components:

### 1. Product Form Component (components/ProductForm.js)

Create a form that:
- Allows selecting from existing product samples or creating a custom product
- Provides input fields for all relevant product attributes (name, description, price, etc.)
- Shows a summary of the selected product or input data
- Handles validation and state management

### 2. Content Type Component (components/ContentType.js)

Implement a component that:
- Provides options to select different types of content to generate
- Includes product descriptions, SEO content, marketing emails, social media posts, etc.
- Allows for image generation selection
- Provides clear explanations of each content type

### 3. Generated Content Component (components/GeneratedContent.js)

Create a component that:
- Displays the generated content in a structured format
- Provides tabs for navigating between different content types