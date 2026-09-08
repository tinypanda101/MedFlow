"""
Hashing and JWT stuff (part of RBAC)
"""

import os
from app.config import settings
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

#will get put in an env file later and an actual secret key generated
SECRET_KEY = settings.secret_key

#Defines algorithm for signing the Json Web Tokens
#HS256 is common for symmetric signing
ALGORITHM = "HS256"

#Expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#need functions to ensure we never store plain passwords
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

#Function creates a JWT acces token with provided data
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    #to_encode is a copy of the input data dictionary, which will be used to create the payload of the JWT
    to_encode = data.copy()

    #check if a time is provided if not use default time
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#This function decodes our webtoken and returns payload as dict
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
