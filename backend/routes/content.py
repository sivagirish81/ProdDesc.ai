from services import openai_service
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

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

@router.post("/products/{product_id}/generate-field")
async def generate_field(
    product_id: str,
    field: str,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database),
    openai_service: OpenAIService = Depends()
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
        product_data = await db.products.find_one({"_id": product_id, "user_id": current_user.id})
        if not product_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        product_data = convert_objectid_to_str(product_data)

        product = Product(**product_data)

        # Generate content for the specified field
        generated_content = await openai_service.generate_missing_field(product, field)

        if field == "features":
            if isinstance(generated_content, str):
                # Split the string into a list of strings
                generated_content = [
                    feature.strip() for feature in generated_content.split("\n") if feature.strip()
                ]

        # Update the database with the generated content
        await db.products.update_one(
            {"_id": product_id},
            {"$set": {field: generated_content}}
        )

        return {
            "message": f"{field} generated successfully.",
            "generated_content": generated_content
        }
    except Exception as e:
        logger.error(f"Error generating field: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating field"
        )
    
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
        
        required_fields = [
            "name", "price", "brand", "category", "basic_description",
            "features", "materials", "colors", "tags", "seo_title",
            "seo_description", "detailed_description", "marketing_copy"
        ]

        missing_fields = {field: None for field in required_fields if not product.get(field)}

        if not missing_fields:
            return {"message": "No missing fields to generate."}

        generated_content = {}
        for field in missing_fields:
            if field in ["seo_title", "seo_description"]:
                generated_content.update(
                    openai_service.generate_seo_content(product, style={"tone": "professional"})
                )
            elif field == "detailed_description":
                generated_content[field] = openai_service.generate_content(product).get("detailed_description")
            elif field == "marketing_copy":
                generated_content[field] = openai_service.generate_marketing_email(product, style={"tone": "engaging"})
            else:
                # Generate other fields (e.g., features, materials, etc.)
                generated_content[field] = openai_service.generate_missing_fields(product, field).get(field)

        # Update the database with the generated content
        if product_id:
            await db.products.update_one(
                {"_id": product_id},
                {"$set": generated_content}
            )

        return {
            "message": "Missing content generated successfully.",
            "generated_content": generated_content
        }
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating content"
        )

@router.post("/products/{product_id}/generate-basic-data")
async def generate_basic_data(
    product_id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Database = Depends(get_database),
    openai_service: OpenAIService = Depends()
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

        description_options = payload.get("descriptionOptions", {})
        image_options = payload.get("imageOptions", {})

        basic_data = await openai_service.generate_basic_data(product, db, product_id, description_options, image_options)

        # Update the product in the database
        await db.products.update_one(
            {"_id": product_id},
            {"$set": basic_data}
        )

        return {
            "message": "Basic data generated successfully.",
            "generated_basic_data": basic_data
        }
    except Exception as e:
        logger.error(f"Error generating basic data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating basic data"
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