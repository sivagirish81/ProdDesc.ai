from sqlalchemy.orm import Session
from ..models import Product
from ..schemas import ProductCreate, ProductUpdate
from ..ai.content_generator import generate_product_content
from typing import List, Optional
from fastapi import HTTPException

def get_user_products(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).filter(Product.user_id == user_id).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate, user_id: int) -> Product:
    db_product = Product(
        name=product.name,
        category=product.category,
        subcategory=product.subcategory,
        basic_description=product.basic_description,
        user_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Product:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True

def generate_section_content(db: Session, product_id: int, section: str, form_data: Optional[dict] = None) -> Product:
    """Generate content for a specific section of a product"""
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Use form data if provided, otherwise use product data
    data = form_data if form_data else product.dict()
    
    # Generate content based on the section
    if section == "product":
        # Generate product description
        product.description = generate_product_description(data)
    elif section == "features":
        # Generate product features
        product.features = generate_product_features(data)
    elif section == "benefits":
        # Generate product benefits
        product.benefits = generate_product_benefits(data)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid section: {section}")
    
    db.commit()
    db.refresh(product)
    return product

def complete_product(db: Session, product_id: int) -> Product:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    # Generate content for all sections
    sections = [
        'basic_description',
        'detailed_description',
        'technical_specifications',
        'key_features',
        'usage_instructions'
    ]
    
    for section in sections:
        generated_content = generate_product_content(
            product_name=db_product.name,
            category=db_product.category,
            subcategory=db_product.subcategory,
            section=section
        )
        setattr(db_product, section, generated_content)
    
    db.commit()
    db.refresh(db_product)
    return db_product 