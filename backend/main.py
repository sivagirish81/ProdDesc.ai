from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from routes.auth import router as auth_router
from routes.products import router as products_router
from routes.content_generation import router as content_generation_router
from utils.auth import get_current_user
from models.user import User
import os
from dotenv import load_dotenv
from database import init_db

# Load environment variables
load_dotenv()

app = FastAPI(title="Product Description API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.proddesc_db

# Mount static files for development
if os.getenv("ENVIRONMENT") != "production":
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Dependency to get database
def get_database():
    return db

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(products_router, prefix="/api", tags=["products"])
app.include_router(content_generation_router, prefix="/api", tags=["content"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the Product Description API"}

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.full_name}, this is a protected route!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 