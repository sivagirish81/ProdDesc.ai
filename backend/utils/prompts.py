def get_prompt_for_field(product, field):
    """Return the appropriate prompt for the given field."""
    prompts = {
        "seo_title": f"Generate an SEO-optimized title for the product: {product.name}.",
        "seo_description": f"Generate an SEO-optimized meta description for the product: {product.name}.",
        "detailed_description": f"Generate a detailed description for the product: {product.name}.",
        "features": f"Suggest additional features for the product: {product.name}.",
        "materials": f"Suggest additional materials for the product: {product.name}.",
        "colors": f"Suggest additional color options for the product: {product.name}.",
        "tags": f"Suggest additional tags for the product: {product.name}.",
        "marketing_copy.email": f"Generate marketing email content for the product: {product.name}.",
        "marketing_copy.social_media.instagram": f"Generate Instagram marketing content for the product: {product.name}.",
        "marketing_copy.social_media.facebook": f"Generate Facebook marketing content for the product: {product.name}.",
        "description": f"Generate a product description for the product: {product.name}.",
    }

    if field not in prompts:
        raise ValueError(f"Field '{field}' is not supported for generation.")
    
    return prompts[field]