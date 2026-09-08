"""
User schema definitions for the application.

These schemas are used for data validation and serialization/deserialization of user-related data.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.models import UserRole

class UserBase(BaseModel):
    username: str = Field(min_length = 3, max_length = 50)
    role: UserRole

class UserCreate(UserBase):
    #when creating a new user they also need a password
    password: str = Field(min_length =3)

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"