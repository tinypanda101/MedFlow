"""
    Async database engine ans session factory for the ORM models to use
"""

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config import settings
#Set database URL to an environmental variable so that is can be easily changed

DATABASE_URL = settings.database_url

#echo = true, enables the logging of all sql statements generted by sqlalchemy
engine = create_async_engine(DATABASE_URL, echo= True)

#Expire_on_commit = false, prevents session from expiring objects after a commit
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
