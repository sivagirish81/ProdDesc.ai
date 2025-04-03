# services/llm_service.py
import openai
import json
from typing import Dict, Any, List
from config import config

class LLMService:
    """
    Service to handle interactions with the LLM API for generating product content
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        openai.api_key = config['OPENAI_API_KEY']
        self.model_name = config['MODEL_NAME']
        self.max_tokens = config['MAX_TOKENS']
        self.temperature = config['TEMPERATURE']
    
    def generate_product_description(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a compelling product description based on product data and style preferences
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences like tone, length, audience
        
        Returns:
        - dict: Generated product description content
        """
        # Create a prompt for the LLM
        prompt = self._create_product_description_prompt(product_data, style)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert eCommerce copywriter who creates compelling product descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract the generated description
            description = response.choices[0].message.content.strip()
            
            return {
                "detailed_description": description
            }
            
        except Exception as e:
            # Handle any errors from the LLM API
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate product description: {str(e)}")
    
    def generate_seo_content(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate SEO-optimized title and meta description
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        
        Returns:
        - dict: Generated SEO content
        """
        # Create a prompt for the LLM
        prompt = self._create_seo_content_prompt(product_data, style)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an SEO expert who creates optimized product titles and meta descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract SEO content
            return self._parse_seo_response(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate SEO content: {str(e)}")
    
    def generate_marketing_email(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate marketing email content for the product
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        
        Returns:
        - dict: Generated marketing email content
        """
        # Create a prompt for the LLM
        prompt = self._create_marketing_email_prompt(product_data, style)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an email marketing specialist who creates compelling product-focused emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract email content
            email_content = response.choices[0].message.content.strip()
            
            return {
                "subject": self._extract_email_subject(email_content),
                "body": self._extract_email_body(email_content)
            }
            
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate marketing email: {str(e)}")
    
    def generate_social_media_content(self, product_data: Dict[str, Any], style: Dict[str, Any], platforms: Dict[str, bool]) -> Dict[str, Any]:
        """
        Generate social media posts for different platforms
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        - platforms (dict): Which platforms to generate content for
        
        Returns:
        - dict: Generated social media content for each platform
        """
        # Create a prompt for the LLM
        prompt = self._create_social_media_prompt(product_data, style, platforms)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a social media manager who creates engaging product posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract social media content
            return self._parse_social_media_response(response.choices[0].message.content, platforms)
            
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate social media content: {str(e)}")
    
    def generate_missing_fields(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate missing fields for a product
        
        Parameters:
        - product_data (dict): Partial product data
        
        Returns:
        - dict: Generated missing fields
        """
        # Create a prompt for the LLM
        prompt = self._create_missing_fields_prompt(product_data)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a product data specialist who completes missing product information accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract missing fields
            return self._parse_missing_fields_response(response.choices[0].message.content, product_data)
            
        except Exception as e:
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate missing fields: {str(e)}")
    
    def complete_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate all content for a product including missing fields and content
        
        Parameters:
        - product_data (dict): Partial product data
        
        Returns:
        - dict: Complete product with all generated content
        """
        # First, generate any missing basic fields
        missing_fields = self.generate_missing_fields(product_data)
        
        # Create a merged product with original data and generated missing fields
        merged_product = {**product_data, **missing_fields}
        
        # Then generate content fields if they're missing
        if not merged_product.get("detailed_description"):
            description = self.generate_product_description(merged_product, {"tone": "professional", "length": "medium"})
            merged_product["detailed_description"] = description.get("detailed_description", "")
        
        if not merged_product.get("seo_title") or not merged_product.get("seo_description"):
            seo_content = self.generate_seo_content(merged_product, {"tone": "professional"})
            if not merged_product.get("seo_title"):
                merged_product["seo_title"] = seo_content.get("title", "")
            if not merged_product.get("seo_description"):
                merged_product["seo_description"] = seo_content.get("description", "")
        
        if not merged_product.get("marketing_copy", {}).get("email"):
            email = self.generate_marketing_email(merged_product, {"tone": "enthusiastic", "length": "medium"})
            if not merged_product.get("marketing_copy"):
                merged_product["marketing_copy"] = {}
            merged_product["marketing_copy"]["email"] = {
                "subject": email.get("subject", ""),
                "body": email.get("body", "")
            }
        
        if not merged_product.get("marketing_copy", {}).get("social_media"):
            social_media = self.generate_social_media_content(
                merged_product, 
                {"tone": "casual", "length": "short"},
                {"instagram": True, "facebook": True, "twitter": True}
            )
            if not merged_product.get("marketing_copy"):
                merged_product["marketing_copy"] = {}
            merged_product["marketing_copy"]["social_media"] = social_media
        
        return merged_product
        
    def generate_product_image(self, product_data: Dict[str, Any], style: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a product image based on product attributes
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict, optional): Style preferences for the image
        
        Returns:
        - dict: Generated image data including URL and prompt used
        """
        # Create a prompt for the image generation
        prompt = self._create_image_generation_prompt(product_data, style or {})
        
        try:
            # Call the OpenAI DALL-E API to generate the image
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # Extract the URL from the response
            image_url = response['data'][0]['url']
            
            return {
                "image_url": image_url,
                "prompt": prompt
            }
            
        except Exception as e:
            print(f"Error calling image generation API: {str(e)}")
            raise Exception(f"Failed to generate product image: {str(e)}")
    
    # Helper methods for creating prompts
    
    def _create_product_description_prompt(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> str:
        """
        Create a prompt for generating a product description
        
        This is where you should implement your prompt engineering strategy.
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        
        Returns:
        - str: Prompt for the LLM
        """
        # Implementation example - detailed prompt crafting
        prompt = f"Create a compelling product description for the following e-commerce product:\n\n"
        
        # Essential product information
        prompt += f"PRODUCT: {product_data.get('name', '')}\n"
        prompt += f"BRAND: {product_data.get('brand', '')}\n"
        prompt += f"PRICE: ${product_data.get('price', '')}\n"
        
        # Add category information
        if product_data.get('category'):
            prompt += f"CATEGORY: {product_data['category']}"
            if product_data.get('subcategory'):
                prompt += f" > {product_data['subcategory']}"
            prompt += "\n"
        
        # Add product features with emphasis
        if product_data.get('features'):
            prompt += "\nKEY FEATURES:\n"
            for feature in product_data['features']:
                prompt += f"• {feature}\n"
        
        # Add materials information
        if product_data.get('materials') and len(product_data.get('materials', [])) > 0:
            prompt += "\nMATERIALS:\n"
            for material in product_data['materials']:
                prompt += f"• {material}\n"
        
        # Add color options
        if product_data.get('colors') and len(product_data.get('colors', [])) > 0:
            prompt += f"\nAVAILABLE COLORS: {', '.join(product_data['colors'])}\n"
        
        # Add existing basic description if available
        if product_data.get('basic_description'):
            prompt += f"\nBASIC PRODUCT INFO: {product_data['basic_description']}\n"
        
        # Add target keywords if available
        if product_data.get('tags'):
            prompt += f"\nTARGET KEYWORDS: {', '.join(product_data['tags'])}\n"
        
        # Style and tone instructions
        prompt += f"\n--- WRITING INSTRUCTIONS ---\n"
        prompt += f"TONE: {style.get('tone', 'professional')}\n"
        
        # Length guidance based on style preference
        if style.get('length') == 'short':
            prompt += "LENGTH: Concise, approximately 75-100 words\n"
        elif style.get('length') == 'long':
            prompt += "LENGTH: Detailed, approximately 200-250 words\n"
        else:  # medium is default
            prompt += "LENGTH: Balanced, approximately 150-175 words\n"
        
        # Target audience customization
        prompt += f"TARGET AUDIENCE: {style.get('audience', 'general consumers')}\n"
        
        # Structure guidance
        prompt += "\nSTRUCTURE:\n"
        prompt += "1. Start with an attention-grabbing opening that highlights a key benefit\n"
        prompt += "2. Describe what the product is and its primary use cases\n"
        prompt += "3. Highlight 3-4 key features and their benefits to the user\n"
        prompt += "4. Include relevant details about quality, materials, or design\n"
        prompt += "5. End with a concise call-to-action or value proposition\n"
        
        # Additional writing guidance
        prompt += "\nADDITIONAL GUIDELINES:\n"
        prompt += "• Use active voice and present tense\n"
        prompt += "• Focus on benefits, not just features\n"
        prompt += "• Create vivid, sensory language where appropriate\n"
        prompt += "• Avoid clichés and generic marketing language\n"
        
        # Keyword integration
        if style.get('keywords'):
            prompt += f"\nPlease naturally incorporate these keywords: {', '.join(style['keywords'])}\n"
        
        # Final output formatting instructions
        prompt += "\nProvide the product description as a cohesive, ready-to-use text without headings or bullet points unless they enhance readability. Don't include any disclaimers or explanations about the content."
        
        return prompt
    
    def _create_seo_content_prompt(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> str:
        """
        Create a prompt for generating SEO content
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy for SEO content
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        prompt = "Generate SEO-optimized title and meta description for a product. Add your implementation."
        
        return prompt
    
    def _create_marketing_email_prompt(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> str:
        """
        Create a prompt for generating marketing email content
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy for marketing emails
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        prompt = "Generate a marketing email for a product. Add your implementation."
        
        return prompt
    
    def _create_social_media_prompt(self, product_data: Dict[str, Any], style: Dict[str, Any], platforms: Dict[str, bool]) -> str:
        """
        Create a prompt for generating social media content
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences
        - platforms (dict): Which platforms to generate content for
        
        Returns:
        - str: Prompt for the LLM
        """
        # Implementation example - detailed social media prompt crafting
        prompt = "I need engaging social media posts to promote the following product:\n\n"
        
        # Essential product information
        prompt += f"Product Name: {product_data.get('name', '')}\n"
        prompt += f"Brand: {product_data.get('brand', '')}\n"
        prompt += f"Price: ${product_data.get('price', '')}\n"
        
        # Product details
        if product_data.get('basic_description'):
            prompt += f"Basic Description: {product_data['basic_description']}\n"
        
        # Key selling points
        if product_data.get('features'):
            prompt += "\nKey Selling Points:\n"
            for feature in product_data['features'][:3]:  # Limit to top 3 features for social
                prompt += f"- {feature}\n"
        
        # Define audience for better targeting
        target_audience = style.get('audience', 'general consumers')
        prompt += f"\nTarget Audience: {target_audience}\n"
        
        # Platform-specific requirements
        prompt += "\nI need content for the following platforms:\n"
        
        if platforms.get('instagram'):
            prompt += """
INSTAGRAM:
- Create an eye-catching caption that works with a product image
- Include 2-3 relevant emojis spaced throughout the text
- Keep the main message under 125 words
- End with a clear call-to-action
- Include 3-5 relevant hashtags at the end (format with # symbol)
- Tone should be visual, aspirational, and lifestyle-focused
"""

        if platforms.get('facebook'):
            prompt += """
FACEBOOK:
- Write a more detailed post (75-100 words)
- Include one question to encourage engagement
- Create a clear value proposition
- End with a specific call-to-action
- Tone should be conversational and informative
- No hashtags needed
"""

        if platforms.get('twitter'):
            prompt += """
TWITTER:
- Create a concise, attention-grabbing tweet (max 280 characters)
- Make it shareable and engaging
- Include 1-2 relevant hashtags integrated into the text
- Include a call-to-action when possible
- Make it conversational, clever or timely when appropriate
"""

        if platforms.get('linkedin'):
            prompt += """
LINKEDIN:
- Create a professional post focused on product benefits (100-150 words)
- Highlight business value, efficiency, or professional benefits
- Use a more formal, business-appropriate tone
- Include one industry insight or trend connection if relevant
- End with a professional call-to-action
- No hashtags needed
"""

        # Style guidance
        prompt += f"\nOverall tone should be: {style.get('tone', 'casual and engaging')}\n"
        
        # Incorporate brand voice
        if product_data.get('brand'):
            prompt += f"The content should reflect {product_data.get('brand')}'s brand identity.\n"
        
        # Hashtag guidance
        if product_data.get('tags'):
            relevant_tags = [tag.replace(' ', '') for tag in product_data.get('tags', [])]
            prompt += f"\nRelevant hashtag keywords: {', '.join(relevant_tags)}\n"
        
        # Output format instructions
        prompt += """
Format your response with clear headings for each platform like this:

INSTAGRAM:
[Instagram post content here with hashtags at the end]

FACEBOOK:
[Facebook post content here]

And so on for each requested platform.
"""
        
        return prompt
    
    def _create_missing_fields_prompt(self, product_data: Dict[str, Any]) -> str:
        """
        Create a prompt for generating missing product fields
        
        Parameters:
        - product_data (dict): Partial product data
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy for generating missing fields
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        prompt = "Generate missing product fields. Add your implementation."
        
        return prompt
    
    def _create_image_generation_prompt(self, product_data: Dict[str, Any], style: Dict[str, Any]) -> str:
        """
        Create a prompt for generating a product image
        
        Parameters:
        - product_data (dict): Product attributes and information
        - style (dict): Style preferences for the image
        
        Returns:
        - str: Prompt for the image generation model
        """
        # TODO: Implement your prompt engineering strategy for image generation
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        prompt = "Generate a product image. Add your implementation."
        
        return prompt
    
    # Helper methods for parsing LLM responses
    
    def _parse_seo_response(self, response_text: str) -> Dict[str, str]:
        """
        Parse the LLM response to extract SEO title and description
        """
        # Implementation example - robust parsing with fallbacks
        result = {"title": "", "description": ""}
        
        # Try to parse structured format first (preferred format)
        title_match = None
        desc_match = None
        
        # Look for "Title:" and "Description:" format
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if line.lower().startswith("title:"):
                title_match = line[6:].strip()
            elif line.lower().startswith("description:"):
                desc_match = line[12:].strip()
        
        # If found both in expected format, return them
        if title_match and desc_match:
            result["title"] = title_match
            result["description"] = desc_match
            return result
            
        # Alternative format - look for section headers or markdown
        sections = response_text.split('\n\n')
        for section in sections:
            section = section.strip()
            if section.lower().startswith("title") or section.lower().startswith("# title"):
                lines = section.split('\n')
                if len(lines) > 1:
                    result["title"] = lines[1].strip()
            elif section.lower().startswith("description") or section.lower().startswith("# description"):
                lines = section.split('\n')
                if len(lines) > 1:
                    result["description"] = lines[1].strip()
        
        # Last resort - if we still don't have both, make best guess from the text
        if not result["title"] or not result["description"]:
            lines = [line.strip() for line in response_text.strip().split('\n') if line.strip()]
            
            # If we don't have a title yet, use the first short line as title
            if not result["title"] and lines:
                for line in lines:
                    if 30 <= len(line) <= 70:  # Good title length
                        result["title"] = line
                        break
                if not result["title"] and lines:  # Still no title, use first line
                    result["title"] = lines[0][:70]
            
            # If we don't have a description yet, use a longer line or combine lines
            if not result["description"] and lines:
                for line in lines:
                    if len(line) >= 120 and line != result["title"]:
                        result["description"] = line[:160]
                        break
                
                # Still no description, combine remaining content
                if not result["description"]:
                    remaining_lines = [l for l in lines if l != result["title"]]
                    if remaining_lines:
                        result["description"] = " ".join(remaining_lines)[:160]
        
        return result
    
    def _extract_email_subject(self, email_content: str) -> str:
        """
        Extract the subject line from the generated email content
        """
        # TODO: Implement your parsing logic for email subject extraction
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        # Basic implementation - assuming "Subject Line:" format
        return "Sample Subject Line"
    
    def _extract_email_body(self, email_content: str) -> str:
        """
        Extract the body from the generated email content
        """
        # TODO: Implement your parsing logic for email body extraction
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        # Basic implementation - assuming "Email Body:" format
        return "Sample email body content."
    
    def _parse_social_media_response(self, response_text: str, platforms: Dict[str, bool]) -> Dict[str, str]:
        """
        Parse the LLM response to extract social media content for each platform
        """
        # Implementation example - robust parsing for different formats
        result = {}
        
        # Split by platform sections and handle different possible formats
        uppercase_platforms = ["INSTAGRAM:", "FACEBOOK:", "TWITTER:", "LINKEDIN:"]
        titlecase_platforms = ["Instagram:", "Facebook:", "Twitter:", "LinkedIn:"]
        
        # Combine all possible platform headers for detection
        all_platform_headers = uppercase_platforms + titlecase_platforms
        
        # Find all section starts
        section_positions = []
        for platform in all_platform_headers:
            pos = response_text.find(platform)
            if pos != -1:
                section_positions.append((pos, platform))
        
        # Sort by position
        section_positions.sort()
        
        # Extract content between sections
        for i, (pos, platform) in enumerate(section_positions):
            # Get platform name in lowercase without colon
            platform_name = platform.lower().replace(":", "")
            
            # Find section end (next section or end of text)
            if i < len(section_positions) - 1:
                next_pos = section_positions[i + 1][0]
                section_text = response_text[pos + len(platform):next_pos].strip()
            else:
                section_text = response_text[pos + len(platform):].strip()
            
            # Store content if platform was requested
            if platform_name in platforms and platforms.get(platform_name):
                result[platform_name] = section_text
        
        # Handle case where no platform headers were found but content exists
        if not result and response_text.strip():
            # If there's content but no headers, try to divide it evenly among requested platforms
            lines = response_text.strip().split('\n')
            requested_platforms = [p for p, v in platforms.items() if v]
            
            if requested_platforms and lines:
                # Simple approach: divide content by blank lines into sections
                sections = []
                current_section = []
                
                for line in lines:
                    if line.strip():
                        current_section.append(line)
                    elif current_section:  # End of a section
                        sections.append('\n'.join(current_section))
                        current_section = []
                
                # Add the last section if it exists
                if current_section:
                    sections.append('\n'.join(current_section))
                
                # Assign sections to platforms
                if len(sections) >= len(requested_platforms):
                    # We have enough sections for each platform
                    for i, platform in enumerate(requested_platforms):
                        result[platform] = sections[i]
                else:
                    # Not enough sections, divide the first one
                    for platform in requested_platforms:
                        result[platform] = response_text.strip()
        
        return result
    
    def _parse_missing_fields_response(self, response_text: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the LLM response to extract missing fields
        """
        # TODO: Implement your parsing logic for extracting missing fields
        # CANDIDATE: IMPLEMENT THIS FUNCTION
        
        # Basic implementation - should be replaced with proper parsing
        return {"category": "Sample Category", "features": ["Sample Feature 1", "Sample Feature 2"]}