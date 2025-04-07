def add_product_info_to_prompt(prompt, product):
    if product.name:
        prompt += f"\nProduct Name: {product.name}"
    if product.brand:
        prompt += f"\nBrand: {product.brand}"
    if product.price:
        prompt += f"\nPrice: ${product.price}"  
    if product.category:    
        prompt += f"\nCategory: {product.category}"
    if product.basic_description:
        prompt += f"\nBasic Description: {product.basic_description}"
    if product.features:
        prompt += f"\nFeatures: {', '.join(product.features)}"
    if product.materials:
        prompt += f"\nMaterials: {', '.join(product.materials)}"
    if product.colors: 
        prompt += f"\nColors: {', '.join(product.colors)}"
    if product.tags:
        prompt += f"\nTags: {', '.join(product.tags)}"  
    return prompt

def get_prompt_for_field(product, field):
    """Return the appropriate prompt for the given field."""
    base_info = f"""
    Product Name: {product.name}
    Brand: {product.brand or 'N/A'}
    Price: ${product.price or 'N/A'}
    Category: {product.category or 'N/A'}
    Basic Description: {product.basic_description or 'N/A'}
    Features: {', '.join(product.features) if product.features else 'N/A'}
    Materials: {', '.join(product.materials) if product.materials else 'N/A'}
    Colors: {', '.join(product.colors) if product.colors else 'N/A'}
    Tags: {', '.join(product.tags) if product.tags else 'N/A'}
    """

    prompts = {
        "seo_title": f"""
        Using the following product information:
        {base_info}
        Generate an SEO-optimized title for the product. The title should be concise, engaging, and include relevant keywords.
        """,

        "seo_description": f"""
        Using the following product information:
        {base_info}
        Generate an SEO-optimized meta description for the product. The description should be engaging, include relevant keywords, and stay within 160 characters.
        """,

        "detailed_description": f"""
        Using the following product information:
        {base_info}
        Generate a detailed product description. Highlight the product's unique features, benefits, and use cases. The tone should be professional and informative.
        """,

        "features": f"""
        Using the following product information:
        {base_info}
        Suggest additional features that would make the product more appealing to customers. 
        Provide a list of 5 features, where each feature is concise and written as a single line.
        """,

        "materials": f"""
        Using the following product information:
        {base_info}
        Suggest additional materials that could be used to manufacture this product. Provide a list of materials.
        """,

        "colors": f"""
        Using the following product information:
        {base_info}
        Suggest additional color options for this product. Provide a list of colors.
        """,

        "tags": f"""
        Using the following product information:
        {base_info}
        Suggest additional tags or keywords that could help categorize and market this product effectively. Provide a list of tags.
        """,

        "marketing_copy.email": f"""
        Using the following product information:
        {base_info}
        Generate an engaging marketing email for this product. The email should highlight the product's key benefits and include a call-to-action to purchase or learn more.
        """,

        "marketing_copy.social_media.instagram": f"""
        Using the following product information:
        {base_info}
        Generate an Instagram post caption for this product. The caption should be engaging, include relevant hashtags, and encourage users to interact with the post.
        """,

        "marketing_copy.social_media.facebook": f"""
        Using the following product information:
        {base_info}
        Generate a Facebook post for this product. The post should highlight the product's key benefits and include a call-to-action to purchase or learn more.
        """,

        "description": f"""
        Using the following product information:
        {base_info}
        Generate a concise and engaging product description. The description should highlight the product's key features and benefits.
        """
    }

    if field not in prompts:
        raise ValueError(f"Field '{field}' is not supported for generation.")
    
    return prompts[field]

def get_prompt_for_basic_product(product):
    """Return a dictionary of prompts for the basic product data."""
    prompt = f"""
        Use the following product information to generate content:
        """
    prompt = add_product_info_to_prompt(prompt, product)

    prompt += f"""
        Generate:
        1. An SEO-optimized title (max 60 characters)
        2. An SEO-optimized meta description (max 160 characters)
        3. A set of five features that highlight the product's unique selling points. Separated by commas.
        4. A set of five materials that could be used to manufacture this product. Separated by commas.
        5. Retain the colors if they exist, otherwise suggest five color options for this product. Separated by commas.
        6. A set of five tags that could be used to market this product. Separated by commas.
        7. A single line product description (max 200 characters)
        Give a line space between each section to enable easy parsing.
        Make sure to: use all the existing data, and suggest new data where necessary.
        Always use the same format. (**1.**, **2.**, **3.**, etc.)
        """
    return prompt

def get_prompt_for_product_description(product, style=None):
    # Implementation example - detailed prompt crafting
    prompt = f"Create a compelling product description for the following e-commerce product:\n\n"
        
    # Add category information
    if product.category:
        prompt += f"CATEGORY: {product.category}\n"
    
    # Add product features with emphasis
    if product.features and len(product.features) > 0:
        prompt += "\nKEY FEATURES:\n"
        for feature in product.features:
            prompt += f"• {feature}\n"
    
    # Add materials information
    if product.materials and len(product.materials) > 0:
        prompt += "\nMATERIALS:\n"
        for material in product.materials:
            prompt += f"• {material}\n"
    
    # Add color options
    if product.colors and len(product.colors) > 0:
        prompt += f"\nAVAILABLE COLORS: {', '.join(product.colors)}\n"
    
    # Add existing basic description if available
    if product.basic_description:
        prompt += f"\nBASIC PRODUCT INFO: {product.basic_description}\n"
    
    # Add target keywords if available
    if product.tags and len(product.tags) > 0:
        prompt += f"\nTARGET KEYWORDS: {', '.join(product.tags)}\n"
    
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

def get_prompt_for_image_generation(product, style=None):
    """Return a prompt for generating product images."""
    prompt = f"""
    Generate a high-quality image of the following product:
    """
    if product.name:
        prompt += f"\nProduct Name: {product.name}"
    if product.brand:
        prompt += f"\nBrand: {product.brand}"
    if product.price:
        prompt += f"\nPrice: ${product.price}"  
    if product.category:    
        prompt += f"\nCategory: {product.category}"
    if product.basic_description:
        prompt += f"\nBasic Description: {product.basic_description}"
    if product.features:
        prompt += f"\nFeatures: {', '.join(product.features)}"
    if product.materials:
        prompt += f"\nMaterials: {', '.join(product.materials)}"
    if product.colors: 
        prompt += f"\nColors: {', '.join(product.colors)}"
    if product.tags:
        prompt += f"\nTags: {', '.join(product.tags)}"  

    prompt += f"""
    \nUse an aesthetic Background: {style.get('background', 'white')}
    """
    prompt += f"""
    \nEnsure {style.get('lighting', 'Natural')} lighting
    """
    prompt += f"""
    Show the product in {style.get('angle', 'front')} angle
    """
    return prompt