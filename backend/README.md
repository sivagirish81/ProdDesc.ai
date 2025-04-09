# Product Description API Backend

This is the backend for the Product Description API, built with FastAPI and MongoDB.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with the following variables:
```
MONGODB_URL=mongodb://localhost:27017
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. Set up test data:
```bash
python scripts/setup_test_data.py
```

## Running the Server

Start the server with:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

The API uses JWT tokens for authentication. To authenticate:

1. Register a new user:
```bash
curl -X POST http://localhost:8000/api/register -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"password","full_name":"User Name"}'
```

2. Login to get a token:
```bash
curl -X POST http://localhost:8000/api/token -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"password"}'
```

3. Use the token in subsequent requests:
```bash
curl -X GET http://localhost:8000/api/products -H "Authorization: Bearer YOUR_TOKEN"
```

## Test User

A test user is created with the setup script:
- Email: test@example.com
- Password: testpassword