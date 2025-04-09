import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

async def create_test_user():
    # Connect to MongoDB
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongodb_url)
    db = client.proddesc_db
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": "test@example.com"})
    if existing_user:
        print(f"Test user already exists with ID: {existing_user['_id']}")
        client.close()
        return existing_user["_id"]
    
    # Create a test user
    password = "testpassword"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    test_user = {
        "email": "test@example.com",
        "hashed_password": hashed_password,
        "full_name": "Test User",
        "is_active": True,
        "is_superuser": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert the test user
    result = await db.users.insert_one(test_user)
    print(f"Test user created with ID: {result.inserted_id}")
    
    # Close the connection
    client.close()
    return result.inserted_id

if __name__ == "__main__":
    asyncio.run(create_test_user()) 