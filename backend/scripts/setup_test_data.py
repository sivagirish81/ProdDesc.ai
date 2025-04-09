import asyncio
from create_test_user import create_test_user
from create_test_product import create_test_product

async def setup_test_data():
    print("Setting up test data...")
    
    # Create test user
    print("\nCreating test user...")
    user_id = await create_test_user()
    
    # Create test product
    print("\nCreating test product...")
    await create_test_product()
    
    print("\nTest data setup complete!")

if __name__ == "__main__":
    asyncio.run(setup_test_data()) 