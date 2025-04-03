from typing import Generator
from pymongo import MongoClient
from pymongo.database import Database
from fastapi import Depends
from database import get_database
from motor.motor_asyncio import AsyncIOMotorClient

def get_database() -> Generator[Database, None, None]:
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    try:
        yield client.proddesc
    finally:
        client.close()

async def get_db():
    """Dependency to get database instance"""
    return get_database() 