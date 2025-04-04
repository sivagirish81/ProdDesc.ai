from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(str(v)):
                raise ValueError("Invalid ObjectId")
            v = ObjectId(str(v))
        return str(v)

class ProductBase(BaseModel):
    name: str
    price: str
    brand: str
    category: str
    basic_description: str
    features: List[str] = Field(default_factory=list)
    materials: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

class ProductPreview(ProductResponse):
    description: Optional[str] = None
    benefits: Optional[str] = None
    specifications: Optional[str] = None
    generated_features: Optional[List[str]] = None
    generated_images: Optional[List[str]] = None

class ContentGenerationRequest(BaseModel):
    section: str
    form_data: Optional[dict] = None 