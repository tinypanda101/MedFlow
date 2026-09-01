"""
For FASTAPI, OAuth etc
TLDR: This is where we put AsyncSessionLocal so its not in every single schema

Enter dependency injection
Design pattern where a piece of code declares what it is dependent on and the framework holds the responsibility for creating and managing that dependency
"""

from collections.abc import AsyncGenerator

import jwt #Json Web Token for Auth stuff

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer #Auth stuff
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import User, UserRole #not added yet this is for RBAC
from app.security import decode_access_token #AuthStuff

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

"""
Yield: Considered like a try-with-resources from java, when a method requries this it will call get_db() which will return the session, then the operations get executed and then after the other function is finished,
it returns here and completes this method which just means it closes the sesion
"""

#Auth stuff goes here later
#Create a dependency that will extract the current user from the JWT token provided in the Auth header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

#Dependency to get the current user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        #note that sub is the standard claim name for subject of a token
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    #finally query database for user w extracter username
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

#Dependency to check if current user has the authorization to access certain things
def require_role(*allowed_roles: UserRole):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(f"Role {current_user.role} is not allowed. ")
            )
        return current_user
    return role_checker