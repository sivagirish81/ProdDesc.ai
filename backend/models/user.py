from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from bson import ObjectId

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: Optional[ObjectId] = None
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    products: List[str] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

class UserInDB(UserBase):
    id: Optional[ObjectId] = None
    hashed_password: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    products: List[str] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

class User(UserBase):
    id: Optional[ObjectId] = None
    created_at: datetime
    updated_at: datetime
    products: List[str] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True
    )

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create a User instance from a dictionary"""
        # Convert _id to id
        if "_id" in data:
            data["id"] = data["_id"]
            del data["_id"]
        
        # Convert ObjectId fields to strings
        if "products" in data:
            data["products"] = [str(product_id) for product_id in data["products"]]
        
        # Ensure datetime fields are properly handled
        if "created_at" in data and isinstance(data["created_at"], datetime):
            data["created_at"] = data["created_at"]
        else:
            data["created_at"] = datetime.utcnow()
            
        if "updated_at" in data and isinstance(data["updated_at"], datetime):
            data["updated_at"] = data["updated_at"]
        else:
            data["updated_at"] = datetime.utcnow()
        
        return cls(**data) 