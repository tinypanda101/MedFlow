"""
For FASTAPI, OAuth etc
TLDR: This is where we put AsyncSessionLocal so its not in every single schema

Enter dependency injection
Design pattern where a piece of code declares what it is dependent on and the framework holds the responsibility for creating and managing that dependency
"""

from collections.abc import AsyncGenerator

# import jwt #Json Web Token for Auth stuff

from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer #Auth stuff
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ASyncSessionLocal
# from app.models import User, UserRole #not added yet this is for RBAC
#from app.security import decode_access_token #AuthStuff

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with ASyncSessionLocal() as session:
        yield session

"""
Yield: Considered like a try-with-resources from java, when a method requries this it will call get_db() which will return the session, then the operations get executed and then after the other function is finished,
it returns here and completes this method which just means it closes the sesion
"""

#Auth stuff goes here later
