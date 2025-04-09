## AI-Powered Product Description Generator

#### Backend Structure
```
backend/
│
├── app.py               # Main FastAPI application
├── requirements.txt     # Python dependencies
├── config.py            # Configuration (add your API keys here)
├── data/
│   └── sample_products.json    # Sample product data
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py   # Service for LLM interactions (implement this)
│   └── product_service.py  # Service for product data operations
│
└── README.md            # Backend setup instructions
```

#### Frontend Structure
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
└── README.md            # Frontend setup instructions
```
