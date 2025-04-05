from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from models.user import User
from models.product import Product
from utils.auth import get_current_user
from dependencies.database import get_database
from services.openai_service import OpenAIService
import logging
from bson import ObjectId, errors as bson_errors

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/products/{product_id}/generate")
async def generate_content(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database),
):
    try:
        # Convert product_id to ObjectId
        try:
            product_id = ObjectId(product_id)
        except bson_errors.InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product ID"
            )

        # Get product
        product = await db.products.find_one({"_id": product_id, "user_id": current_user.id})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Generate content (placeholder logic)
        generated_content = {
            "description": "Generated product description",
            "seo_title": "Generated SEO title",
            "meta_description": "Generated meta description",
        }

        # Update product with generated content
        await db.products.update_one(
            {"_id": product_id},
            {"$set": generated_content}
        )

        return {"message": "Content generated successfully", "generated_content": generated_content}
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating content"
        )

@router.post("/complete/{product_id}")
async def complete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database),
    openai_service: OpenAIService = Depends()
):
    try:
        # Get product
        product = db.products.find_one({
            "_id": product_id,
            "user_id": current_user.id
        })
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Complete product with missing fields
        completed_product = await openai_service.complete_product(product)
        
        # Update product with completed fields
        db.products.update_one(
            {"_id": product_id},
            {"$set": completed_product}
        )

        return completed_product
    except Exception as e:
        logger.error(f"Error completing product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error completing product"
        ) 