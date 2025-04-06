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
        Generate:
        1. An SEO-optimized title (max 60 characters)
        2. An SEO-optimized meta description (max 160 characters)
        3. A set of five features that highlight the product's unique selling points. Separated by commas.
        4. A set of five materials that could be used to manufacture this product. Separated by commas.
        5. Retain the colors if they exist, otherwise suggest five color options for this product. Separated by commas.
        6. A set of five tags that could be used to market this product. Separated by commas.
        7. A single line product description (max 200 characters)
        8. A detailed product description (250-400 words) : This should be a comprehensive overview of the product, including its features, benefits, and use cases. It should be engaging and informative, written in a professional tone.
        Give a line space between each section to enable easy parsing.
        Make sure to: use all the existing data, and suggest new data where necessary.
        Always use the same format. (**1.**, **2.**, **3.**, etc.)
        """
    return prompt