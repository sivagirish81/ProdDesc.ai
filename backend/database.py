from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.proddesc_db

async def init_db():
    """Initialize database and create indexes if needed"""
    # Create indexes for users collection
    await db.users.create_index("email", unique=True)
    
    # Create indexes for products collection
    await db.products.create_index("user_id")
    await db.products.create_index([("user_id", 1), ("created_at", -1)])
    
    print("Database initialized successfully")

def get_database():
    """Get database instance"""
    return db 