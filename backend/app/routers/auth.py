"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import User, UserRole
from app.schemas.user import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

#Step 1 set up router
router = APIRouter(prefix='/auth', tags=["auth"])

#Step2 is to define login endpoint which accepts username and password
@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    #check to verify if pass is correct
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #set access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")


#function to register a new user, will require the admin role to use
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
)-> User:
    #checking if user already exists
    existing = await db.execute(select(User).where(User.username == payload.username))
    if existing.scalar_one_or_none is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {payload.username!r} is already taken",
        )

    #Create a new user object with the providede username role and hashed password
    user = User(
        username=payload.username,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
