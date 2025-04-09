# AI-Powered Product Description Generator

This project is an AI-powered tool designed to generate compelling, SEO-optimized product descriptions, marketing copy, and product images based on basic product information. It consists of a **React-based frontend** and a **FastAPI backend** that integrates with an LLM (Large Language Model) API for content generation.

---

## Features

- **Product Description Generation**: Create detailed, SEO-friendly product descriptions.
- **Marketing Copy**: Generate engaging marketing emails and social media content.
- **Image Generation**: Generate product images based on descriptions.
- **Customizable Style**: Configure tone, length, and audience preferences for generated content.
- **User-Friendly Interface**: Intuitive React-based frontend for seamless interaction.

---

## Project Structure

### Backend
```
backend/
│
├── app.py               # Main FastAPI application
├── requirements.txt     # Python dependencies
├── config.py            # Configuration (API keys, environment variables)
├── data/
│   └── sample_products.json    # Sample product data
│
├── services/
│   ├── llm_service.py   # Service for LLM interactions
│   ├── openai_service.py # Service for OpenAI API interactions
│   └── product_service.py  # Service for product data operations
│
├── routes/
│   ├── auth.py          # Authentication routes
│   ├── content.py       # Routes for content generation
│   └── products.py      # Routes for product management
│
└── utils/
    ├── prompts.py       # Prompt engineering utilities
    └── converter.py     # Utility for data conversion
```

### Frontend
```
frontend/
│
├── public/
│   └── index.html       # HTML entry point
│
├── src/
│   ├── App.js           # Main application component
│   ├── index.js         # Entry point
│   ├── components/
│   │   ├── ProductForm.js   # Form for product data input
│   │   ├── ContentType.js   # Content type selector
│   │   ├── GeneratedContent.js  # Display for generated content
│   │   └── StyleOptions.js  # Style and tone configuration
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

---

## Environment Setup

### Prerequisites

- **Backend**: Python 3.11+, MongoDB, and OpenAI API key.
- **Frontend**: Node.js 16+ and npm.

---

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a directory for images**:
   ```bash
   mkdir uploads/images
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory similar to the .env.example.

5. **Run the backend server**:
   ```bash
   uvicorn app:app --reload
   ```

   The backend will be available at `http://localhost:8000`.

---

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env.local` file in the frontend directory with the following:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run the frontend development server**:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

---

## Usage

1. **Input Product Data**:
   - Use the form in the frontend to input basic product details (e.g., name, category, features).

2. **Generate Content**:
   - Select the type of content to generate (e.g., product description, marketing copy).
   - Configure style preferences (tone, length, audience).

3. **View and Edit**:
   - Review the generated content and make edits if necessary.

4. **Save and Export**:
   - Save the content to the database or export it for use in your e-commerce platform.

---

## Development

### Backend
- **Run Tests**:
  ```bash
  pytest
  ```

- **Linting**:
  ```bash
  flake8
  ```

### Frontend
- **Run Tests**:
  ```bash
  npm test
  ```

- **Linting**:
  ```bash
  npm run lint
  ```

---

## Environment Variables

### Backend
- `OPENAI_API_KEY`: API key for OpenAI.
- `MONGO_URI`: MongoDB connection string.

### Frontend
- `REACT_APP_API_URL`: Base URL for the backend API.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.

---

## License

This project is licensed under the ISC License. See the LICENSE file for details.

---

## Acknowledgments

- **OpenAI**: For providing the LLM API.
- **FastAPI**: For the backend framework.
- **React**: For the frontend framework.
   ```

