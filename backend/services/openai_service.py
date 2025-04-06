from openai import AsyncOpenAI
from models.product import Product
import os
from typing import Dict, Any
from utils.prompts import get_prompt_for_field, get_prompt_for_basic_product
import logging
from pymongo.database import Database
from utils.converter import convert_objectid_to_str
import re

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini-2024-07-18"

    def _parse_list(self, section: str) -> list:
        """Parse a section into a clean list of items."""
        if not section:
            return []
        # Remove any extra formatting (e.g., **bold text**) and split by commas
        section = re.sub(r"\*\*.*?\*\*", "", section).strip()
        return [item.strip() for item in section.split(",") if item.strip()]
    
    async def generate_content(self, product: Product, db, product_id: str) -> Dict[str, Any]:
        try:
            """Generate SEO and marketing content for a product."""
            prompt = get_prompt_for_basic_product(product)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional product content writer and SEO expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            # Parse the response into structured content
            content = response.choices[0].message.content

            logger.info(f"Generated content: {content}")
            content = re.sub(r"\*\*\d+\.\*\*", "", content).strip()
            sections = content.split("\n\n")
            
            # Map the parsed content to product fields
            generated_data = {
                "seo_title": sections[0].strip() if len(sections) > 0 else "",
                "seo_description": sections[1].strip() if len(sections) > 1 else "",
                "features": self._parse_list(sections[2]) if len(sections) > 2 else [],
                "materials": self._parse_list(sections[3]) if len(sections) > 3 else [],
                "colors": self._parse_list(sections[4]) if len(sections) > 4 else [],
                "tags": self._parse_list(sections[5]) if len(sections) > 5 else [],
                "basic_description": sections[6].strip() if len(sections) > 6 else "",
                "detailed_description": "\n\n".join(sections[7:]).strip() if len(sections) > 6 else "",
            }

            logger.info(f"Generated content: {generated_data}")
            logger.info(f"Product ID: {product_id}")

            # Update the product in the database
            await db.products.update_one(
                {"_id": product_id},
                {"$set": generated_data}
            )

            logger.info(f"Generated content stored successfully for product: {product.name}")
            return generated_data
        except Exception as e:
            logger.error(f"Error generating content for product: {str(e)}")
            raise ValueError(f"Error generating content: {str(e)}")
    
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
        
    async def generate_basic_data(self, product: dict, db : Database, product_id : str) -> Dict[str, Any]:
        """Generate basic data for a product and generate product image."""
        try:
            # Convert the product dictionary to a Product object
            product = convert_objectid_to_str(product)
            product_obj = Product(**product)
            return await self.generate_content(product_obj, db, product_id)
        except Exception as e:
            logger.error(f"Error generating basic data: {str(e)}")
            raise ValueError(f"Error generating basic data: {str(e)}")