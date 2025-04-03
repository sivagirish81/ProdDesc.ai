from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union

from services.llm_service import LLMService
from services.product_service import ProductService

app = FastAPI(title="AI Product Description Generator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize services
product_service = ProductService()
llm_service = LLMService()

# Define request models
class ContentStyle(BaseModel):
    tone: str = "professional"  # professional, casual, enthusiastic, etc.
    length: str = "medium"  # short, medium, long
    audience: str = "general"  # general, technical, beginner, etc.
    keywords: List[str] = []

class SocialMediaConfig(BaseModel):
    instagram: bool = True
    facebook: bool = True
    twitter: bool = True
    linkedin: bool = False

class ContentRequest(BaseModel):
    product_id: Optional[str] = None
    product_data: Optional[Dict[str, Any]] = None
    content_types: List[str] = ["product_description"]  # product_description, seo, marketing_email, social_media, missing_fields
    style: ContentStyle = ContentStyle()
    social_media: Optional[SocialMediaConfig] = None

@app.get("/api/products")
async def get_products():
    """
    Return the full product catalog
    """
    products = product_service.get_all_products()
    return products

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """
    Get a specific product by ID
    """
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/generate-content")
async def generate_content(request: ContentRequest):
    """
    Generate content for a product based on the requested content types
    """
    try:
        # Determine the product data to use
        product_data = None
        if request.product_id:
            # Get product data from the database
            product_data = product_service.get_product_by_id(request.product_id)
            if not product_data:
                raise HTTPException(status_code=404, detail="Product not found")
        elif request.product_data:
            # Use the provided product data
            product_data = request.product_data
        else:
            raise HTTPException(status_code=400, detail="Either product_id or product_data must be provided")
        
        # Generate the requested content
        generated_content = {}
        for content_type in request.content_types:
            if content_type == "product_description":
                generated_content["product_description"] = llm_service.generate_product_description(
                    product_data, request.style.dict()
                )
            elif content_type == "seo":
                generated_content["seo"] = llm_service.generate_seo_content(
                    product_data, request.style.dict()
                )
            elif content_type == "marketing_email":
                generated_content["marketing_email"] = llm_service.generate_marketing_email(
                    product_data, request.style.dict()
                )
            elif content_type == "social_media":
                if not request.social_media:
                    request.social_media = SocialMediaConfig()
                generated_content["social_media"] = llm_service.generate_social_media_content(
                    product_data, request.style.dict(), request.social_media.dict()
                )
            elif content_type == "missing_fields":
                generated_content["missing_fields"] = llm_service.generate_missing_fields(
                    product_data
                )
            else:
                raise HTTPException(status_code=400, detail=f"Unknown content type: {content_type}")
        
        return {
            "product": product_data,
            "generated_content": generated_content
        }
    
    except Exception as e:
        # Handle any errors from the LLM API
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-image")
async def generate_image(request: Dict[str, Any]):
    """
    Generate a product image based on product data
    """
    try:
        product_data = request.get("product_data")
        if not product_data:
            raise HTTPException(status_code=400, detail="Product data must be provided")
        
        # Optional parameters
        style = request.get("style", {})
        
        # Generate image
        image_result = llm_service.generate_product_image(product_data, style)
        
        return {
            "product": product_data,
            "image_result": image_result
        }
    
    except Exception as e:
        # Handle any errors from the LLM or Image Generation API
        raise HTTPException(status_code=500, detail=str(e))

# Custom exception handler for more user-friendly error messages
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return {
        "error": str(exc),
        "message": "An error occurred while processing your request"
    }

if __name__ == "__main__":
    # Run the API with uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)