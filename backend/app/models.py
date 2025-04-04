from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Product(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectId
    name: str
    price: str
    brand: str
    category: str
    basic_description: str
    description: Optional[str] = None
    benefits: Optional[str] = None
    specifications: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    materials: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    generated_features: Optional[List[str]] = None
    generated_images: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 