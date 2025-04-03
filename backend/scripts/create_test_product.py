import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def create_test_product():
    # Connect to MongoDB
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongodb_url)
    db = client.proddesc
    
    # First, find a user to associate with the product
    user = await db.users.find_one()
    if not user:
        print("No users found in the database. Please create a user first.")
        client.close()
        return
    
    user_id = user["_id"]
    print(f"Found user: {user.get('email')} with ID: {user_id}")
    
    # Create a test product
    test_product = {
        "user_id": user_id,
        "name": "Test Product",
        "price": 99.99,
        "basic_description": "A test product for development purposes",
        "content": {
            "product_description": "This is a detailed description of the test product.",
            "seo_title": "Test Product - Best Quality",
            "meta_description": "Discover our amazing test product with the best quality and features.",
            "email_marketing": "Don't miss out on our amazing test product! Limited time offer.",
            "social_media": "Check out our new test product! #TestProduct #NewArrival",
            "features_list": "1. High Quality\n2. Durable\n3. Affordable",
            "image_description": "A professional product photo showing the test product in use."
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert the test product
    result = await db.products.insert_one(test_product)
    print(f"Test product created with ID: {result.inserted_id}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_product()) 