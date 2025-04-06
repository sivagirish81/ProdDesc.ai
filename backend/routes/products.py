from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from pymongo.database import Database
from models.product import Product, ProductCreate
from models.user import User
from utils.auth import get_current_user
from services.image_service import ImageService
from dependencies.database import get_database
import logging
from datetime import datetime
from bson import ObjectId, errors as bson_errors
from motor.motor_asyncio import AsyncIOMotorCursor, AsyncIOMotorDatabase
from utils.converter import convert_objectid_to_str

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/products", response_model=Product)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    try:
        # Create new product with user_id

        user_id_str = str(current_user.id)

        new_product = Product(
            user_id=user_id_str,
            **product.model_dump()
        )
        
        # Insert into database
        product_dict = new_product.to_dict()
        result = await db.products.insert_one(product_dict)
        
        # Get the created product
        created_product = await db.products.find_one({"_id": result.inserted_id})
        return Product.from_dict(created_product)
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product"
        )

@router.get("/products", response_model=List[Product])
async def get_products(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all products for the current user"""
    try:
        # Convert string ID to ObjectId
        user_id = ObjectId(current_user.id)
        
        # Get async cursor
        cursor: AsyncIOMotorCursor = db.products.find({"user_id": user_id})
        
        # Convert cursor to list using Motor's async method
        product_docs = await cursor.to_list(length=1000)  # Adjust length as needed
        
        # Convert MongoDB documents to Pydantic models
        return [Product.from_dict(doc) for doc in product_docs]
        
    except bson_errors.InvalidId as e:
        logger.error(f"Invalid ID error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching products"
        )

@router.get("/products/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get a specific product by ID"""
    try:
        product = await db.products.find_one({
            "_id": ObjectId(product_id),
            "user_id": ObjectId(current_user.id)
        })
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return Product.from_dict(product)
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching product"
        )

@router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product: Product,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """Update a product"""
    try:
        # Check if product exists and belongs to user
        existing_product = await db.products.find_one({
            "_id": ObjectId(product_id),
            "user_id": ObjectId(current_user.id)
        })
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        product.id = product_id
        product.user_id = current_user.id
        product.updated_at = datetime.utcnow()

        logger.info(f"Updating product: {product.to_dict()}")
        
        await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product.to_dict()}
        )

        # Fetch the updated product
        updated_product = await db.products.find_one({"_id": product_id})

        # Convert ObjectId fields to strings
        updated_product = convert_objectid_to_str(updated_product)

        return {
            "message": "Product updated successfully.",
            "product": updated_product
        }
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating product"
        )

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """Delete a product"""
    try:
        result = await db.products.delete_one({
            "_id": ObjectId(product_id),
            "user_id": ObjectId(current_user.id)
        })
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {"message": "Product deleted successfully"}
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting product"
        )

@router.post("/products/{product_id}/image")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database),
    image_service: ImageService = Depends()
):
    try:
        # Check if product exists and belongs to user
        product = await db.products.find_one({
            "_id": ObjectId(product_id),
            "user_id": ObjectId(current_user.id)
        })
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Delete old image if exists
        if product.get("image_url"):
            await image_service.delete_image(product["image_url"])

        # Upload new image
        image_url = await image_service.upload_image(file, str(current_user.id))
        if not image_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading image"
            )

        # Update product with new image URL
        await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"image_url": image_url}}
        )

        return {"image_url": image_url}
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    except Exception as e:
        logger.error(f"Error uploading product image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading product image"
        ) 