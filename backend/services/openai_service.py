from openai import AsyncOpenAI
from models.product import Product
import os
from typing import Dict, Any

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