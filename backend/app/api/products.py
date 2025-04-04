from fastapi import APIRouter, Depends, HTTPException, status, Body, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..models import Product, User
from ..schemas import ProductCreate, ProductUpdate, ProductResponse, ProductPreview, ContentGenerationRequest
from ..auth import get_current_user
from ..services import product_service
from bson import ObjectId
from datetime import datetime

router = APIRouter()

def parse_product_id(product_id: str) -> int:
    """Parse product ID, handling both numeric and custom formats"""
    if isinstance(product_id, int):
        return product_id
    if product_id.startswith('custom-'):
        try:
            return int(product_id.split('-')[1])
        except (IndexError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid product ID format")
    try:
        return int(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all products for the current user"""
    products = await db["products"].find(
        {"user_id": current_user.id}
    ).skip(skip).limit(limit).to_list(length=limit)
    return products

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new product"""
    try:
        product_dict = product.model_dump()
        product_dict["user_id"] = current_user.id
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        
        result = await db["products"].insert_one(product_dict)
        created_product = await db["products"].find_one({"_id": result.inserted_id})
        
        return created_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{product_id}", response_model=ProductPreview)
async def get_product(
    product_id: str,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific product with all its details"""
    try:
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if str(product["user_id"]) != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized to access this product")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=ProductPreview)
def update_product(
    product_id: str,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product"""
    parsed_id = parse_product_id(product_id)
    product = product_service.get_product(db, parsed_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    return product_service.update_product(db, parsed_id, product_update)

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a product"""
    parsed_id = parse_product_id(product_id)
    product = product_service.get_product(db, parsed_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    product_service.delete_product(db, parsed_id)
    return {"message": "Product deleted successfully"}

class GenerateContentRequest(BaseModel):
    section: str
    form_data: dict

@router.post("/{product_id}/generate", response_model=ProductPreview)
async def generate_content(
    product_id: str,
    request: ContentGenerationRequest,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate content for a specific section of a product"""
    try:
        # Get the existing product
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if str(product["user_id"]) != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")

        # Generate content based on section
        if request.section == "product":
            # Generate product description
            product["description"] = "Generated description based on: " + request.form_data.get("basic_description", "")
        elif request.section == "features":
            # Generate features
            product["generated_features"] = ["Generated feature 1", "Generated feature 2"]
        elif request.section == "benefits":
            # Generate benefits
            product["benefits"] = "Generated benefits based on features"
        
        # Update the product
        product["updated_at"] = datetime.utcnow()
        await db["products"].replace_one({"_id": ObjectId(product_id)}, product)
        
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{product_id}/complete", response_model=ProductPreview)
def complete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Complete all sections of a product"""
    parsed_id = parse_product_id(product_id)
    product = product_service.get_product(db, parsed_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this product")
    
    # Complete all sections
    updated_product = product_service.complete_product(db, parsed_id)
    return updated_product 