from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from bson import ObjectId

class MarketingCopy(BaseModel):
    email: str = ""
    social_media: Dict[str, str] = {
        "instagram": "",
        "facebook": ""
    }

class ProductBase(BaseModel):
    name: str
    price: float
    brand: str = ""
    basic_description: str
    category: str = ""
    subcategory: str = ""
    features: List[str] = []
    materials: List[str] = []
    colors: List[str] = []
    tags: List[str] = []

class ProductCreate(ProductBase):
    pass

class Product(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: str = ""
    price: float = 0.0
    brand: str = ""
    basic_description: str = ""
    category: str = ""
    subcategory: str = ""
    features: List[str] = []
    materials: List[str] = []
    colors: List[str] = []
    tags: List[str] = []
    image_url: str = ""
    seo_title: str = ""
    seo_description: str = ""
    detailed_description: str = ""
    marketing_copy: MarketingCopy = MarketingCopy()
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    is_completed: bool = False
    content: Dict[str, Any] = {}

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
            "basic_description": self.basic_description,
            "category": self.category,
            "subcategory": self.subcategory,
            "features": self.features,
            "materials": self.materials,
            "colors": self.colors,
            "tags": self.tags,
            "image_url": self.image_url,
            "seo_title": self.seo_title,
            "seo_description": self.seo_description,
            "detailed_description": self.detailed_description,
            "marketing_copy": self.marketing_copy.model_dump(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_completed": self.is_completed,
            "content": self.content
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        if self.user_id:
            data["user_id"] = ObjectId(self.user_id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        id_str = str(data.pop("_id")) if "_id" in data else None
        user_id_str = str(data.pop("user_id")) if "user_id" in data else None
        
        # Handle marketing_copy if it exists
        if "marketing_copy" in data and isinstance(data["marketing_copy"], dict):
            data["marketing_copy"] = MarketingCopy(**data["marketing_copy"])
        
        return cls(
            id=id_str,
            user_id=user_id_str,
            **data
        ) 