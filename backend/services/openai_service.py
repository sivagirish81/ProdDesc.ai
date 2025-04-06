from openai import AsyncOpenAI
from models.product import Product
import os
from typing import Dict, Any
from utils.prompts import get_prompt_for_field
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"

    async def generate_content(self, product: Product) -> Dict[str, Any]:
        """Generate SEO and marketing content for a product."""
        prompt = f"""
        Generate comprehensive content for the following product:
        
        Name: {product.name}
        Brand: {product.brand}
        Price: ${product.price}
        Category: {product.category}
        Subcategory: {product.subcategory}
        Basic Description: {product.basic_description}
        Features: {', '.join(product.features)}
        Materials: {', '.join(product.materials)}
        Colors: {', '.join(product.colors)}
        Tags: {', '.join(product.tags)}

        Please generate:
        1. An SEO-optimized title (max 60 characters)
        2. An SEO-optimized meta description (max 160 characters)
        3. A detailed product description (500-1000 words)
        4. Marketing copy for email and social media (Instagram and Facebook)
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional product content writer and SEO expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content = response.choices[0].message.content
        
        # Parse the response into structured content
        # This is a simple example - you might want to make this more robust
        sections = content.split("\n\n")
        
        return {
            "seo_title": sections[0].strip(),
            "seo_description": sections[1].strip(),
            "detailed_description": sections[2].strip(),
            "marketing_copy": {
                "email": sections[3].strip(),
                "social_media": {
                    "instagram": sections[4].strip(),
                    "facebook": sections[5].strip()
                }
            }
        }

    async def complete_product(self, product: Product) -> Dict[str, Any]:
        """Complete missing fields in a product using AI."""
        prompt = f"""
        Complete the following product information:
        
        Name: {product.name}
        Brand: {product.brand}
        Price: ${product.price}
        Category: {product.category}
        Subcategory: {product.subcategory}
        Basic Description: {product.basic_description}
        Features: {', '.join(product.features)}
        Materials: {', '.join(product.materials)}
        Colors: {', '.join(product.colors)}
        Tags: {', '.join(product.tags)}

        Please suggest:
        1. Additional features that would be relevant
        2. Additional materials that might be used
        3. Additional color options
        4. Additional relevant tags
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a product development expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        
        # Parse the response into structured content
        # This is a simple example - you might want to make this more robust
        sections = content.split("\n\n")
        
        return {
            "features": product.features + [f.strip() for f in sections[0].split(",")],
            "materials": product.materials + [m.strip() for m in sections[1].split(",")],
            "colors": product.colors + [c.strip() for c in sections[2].split(",")],
            "tags": product.tags + [t.strip() for t in sections[3].split(",")]
        } 
    
    async def generate_missing_fields(self, product: Product, field: str) -> Dict[str, Any]:
        """Generate missing fields for a product."""
        # This method can be similar to complete_product or can be customized

        return await self.complete_product(product)
    
    async def generate_missing_field(self, product: Product, field: str) -> Any:
        """Generate content for a specific field of a product."""
        try:
            # Get the appropriate prompt for the field
            logger.info(f"Generating content for field: {field}")
            prompt = get_prompt_for_field(product, field)

            # Call the OpenAI API with the prompt
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a product content generation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Extract and return the generated content
            content = response.choices[0].message.content.strip()
            return content
        except Exception as e:
            raise ValueError(f"Error generating content for field '{field}': {str(e)}")