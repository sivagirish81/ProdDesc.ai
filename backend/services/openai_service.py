from openai import AsyncOpenAI
from models.product import Product
import os
from typing import Dict, Any
from utils.prompts import get_prompt_for_field, get_prompt_for_basic_product, get_prompt_for_product_description, get_prompt_for_image_generation
import logging
from pymongo.database import Database
from utils.converter import convert_objectid_to_str
import re
import requests
import uuid
import asyncio
import openai

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini-2024-07-18"
        self.image_model = "dall-e-3"
        self.upload_folder = os.path.join(os.getcwd(), "uploads", "images")

    def _parse_list(self, section: str) -> list:
        """Parse a section into a clean list of items."""
        if not section:
            return []
        # Remove any extra formatting (e.g., **bold text**) and split by commas
        section = re.sub(r"\*\*.*?\*\*", "", section).strip()
        return [item.strip() for item in section.split(",") if item.strip()]
    
    async def generate_content(self, product: Product, db, product_id: str, description_options: dict, image_options: dict) -> Dict[str, Any]:
        try:
            """Generate SEO and marketing content for a product."""
            basic_prompt = get_prompt_for_basic_product(product)
            description_prompt = get_prompt_for_product_description(product, style={"tone": description_options["tone"], "length": description_options["length"], "audience": description_options["audience"]})
            image_generation_prompt = get_prompt_for_image_generation(product, style={"background": image_options["background"], "lighting": image_options["lighting"], "angle": image_options["angle"]})

            logger.info(f"Detailed description prompt: {description_prompt}")
            general_task = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional product content writer and SEO expert."},
                    {"role": "user", "content": basic_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            description_task = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional product description writer."},
                    {"role": "user", "content": description_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            logger.info(f"Image generation prompt: {image_generation_prompt}")
            product_image_task = asyncio.to_thread(self.generate_image, image_generation_prompt)

            general_response, description_response, product_image_response = await asyncio.gather(general_task, description_task, product_image_task)
            # Parse the general response into structured content

            generated_image_url = product_image_response["data"][0]["url"]
            stored_image_url = await self.get_image_data(generated_image_url)
            
            logger.info(f"General response: {general_response}")
            logger.info(f"Description response: {description_response}")
            general_content = general_response.choices[0].message.content
            general_content = re.sub(r"\*\*\d+\.\*\*", "", general_content).strip()
            sections = general_content.split("\n\n")

            # Parse the product description response
            product_description = description_response.choices[0].message.content.strip()

            # Map the parsed content to product fields
            generated_data = {
                "seo_title": sections[0].strip() if len(sections) > 0 else "",
                "seo_description": sections[1].strip() if len(sections) > 1 else "",
                "features": self._parse_list(sections[2]) if len(sections) > 2 else [],
                "materials": self._parse_list(sections[3]) if len(sections) > 3 else [],
                "colors": self._parse_list(sections[4]) if len(sections) > 4 else [],
                "tags": self._parse_list(sections[5]) if len(sections) > 5 else [],
                "basic_description": sections[6].strip() if len(sections) > 6 else "",
                "detailed_description": product_description,
                "image_url": stored_image_url,
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
        
    async def generate_basic_data(self, product: dict, db : Database, product_id : str, description_options: dict, image_options: dict) -> Dict[str, Any]:
        """Generate basic data for a product and generate product image."""
        try:
            # Convert the product dictionary to a Product object
            product = convert_objectid_to_str(product)
            product_obj = Product(**product)
            return await self.generate_content(product_obj, db, product_id, description_options, image_options)
        except Exception as e:
            logger.error(f"Error generating basic data: {str(e)}")
            raise ValueError(f"Error generating basic data: {str(e)}")
        
    def generate_image(self, prompt: str) -> str:
        """
        Generate an image based on the given prompt, save it to the uploads/images folder,
        and return the URL for accessing the image.
        """
        try:
            # Call OpenAI's image generation API
            response =  openai.Image.create(
                model=self.image_model,
                prompt=prompt,
                n=1,  # Generate one image
                size="512x512"  # Image size
            )

            # Extract the image URL from the response
            image_url = response["data"][0]["url"]

            # Download the image
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code != 200:
                raise ValueError(f"Failed to download the generated image: {image_response.status_code}")

            # Generate a unique filename for the image
            filename = f"{uuid.uuid4().hex}.png"
            file_path = os.path.join(self.upload_folder, filename)

            # Save the image to the uploads/images folder
            with open(file_path, "wb") as image_file:
                for chunk in image_response.iter_content(1024):
                    image_file.write(chunk)

            # Return the URL for accessing the image
            image_access_url = f"{self.base_url}/uploads/images/{filename}"
            return image_access_url

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise ValueError(f"Error generating image: {str(e)}")