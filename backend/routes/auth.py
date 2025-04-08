from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database
from datetime import datetime, timedelta
from typing import Optional
from models.user import User, UserCreate, UserResponse
from utils.auth import (
    verify_password,
    get_password_hash,
    create_tokens,
    get_current_user,
    refresh_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from pydantic import BaseModel, EmailStr
from dependencies.database import get_database
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refresh_token: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Database = Depends(get_database)):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    now = datetime.utcnow()
    user_dict = {
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "full_name": user.full_name,
        "is_active": True,
        "is_superuser": False,
        "created_at": now,
        "updated_at": now,
        "products": []
    }
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = result.inserted_id
    
    # Create response without hashed_password
    response_dict = {k: v for k, v in user_dict.items() if k != "hashed_password"}
    return UserResponse(**response_dict)

@router.post("/login/json", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Login with email and password"""
    try:
        # Find user by email
        user_data = await db.users.find_one({"email": login_data.email})
        logger.info(f"User data: {user_data}")
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user_data["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create tokens
        access_token, refresh_token = create_tokens(data={"sub": str(user_data["_id"])})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(get_database)
):
    # Find user by email
    user_data = db.users.find_one({"email": form_data.username})
    
    # Check if user exists and password is correct
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user_data.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create tokens
    access_token, refresh_token = create_tokens(data={"sub": user_data["email"]})
    
    # Create user response
    user_response = UserResponse(
        id=user_data["_id"],  # MongoDB's _id field
        email=user_data["email"],
        full_name=user_data["full_name"],
        is_active=user_data.get("is_active", True),
        is_superuser=user_data.get("is_superuser", False),
        created_at=user_data.get("created_at", datetime.utcnow()),
        updated_at=user_data.get("updated_at", datetime.utcnow()),
        products=user_data.get("products", [])
    )
    
    # Update last login time
    db.users.update_one(
        {"_id": user_data["_id"]},
        {"$set": {"updated_at": datetime.utcnow()}}
    )
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user_response
    )

@router.post("/token", response_model=Token)
async def login_legacy(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(get_database)
):
    user_data = db.users.find_one({"email": form_data.username})
    if not user_data or not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create both access and refresh tokens
    access_token, refresh_token = create_tokens(data={"sub": user_data["email"]})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    try:
        # Verify refresh token and get new access token
        access_token = refresh_access_token(token_data.refresh_token)
        return Token(
            access_token=access_token,
            refresh_token=token_data.refresh_token,
            token_type="bearer"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        products=current_user.products
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user"""
    try:
        # In a real application, you might want to blacklist the token
        # or perform other cleanup operations
        return {"message": "Successfully logged out"}
    except Exception as e:
        # Even if there's an error, we want to return a success message
        # to ensure the frontend can proceed with the logout flow
        logger.error(f"Error during logout: {str(e)}")
        return {"message": "Successfully logged out"} 