"""
    Async database engine ans session factory for the ORM models to use
"""

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

#Set database URL to an environmental variable so that is can be easily changed

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    #EX: postgresql+asyncpg://<yourusername>:<yourpassword>@localhost:5432/robopulse_dev_2478
    "postgresql+asyncpg://postgres:Binx123@localhost:5432/medflow"
)

#echo = true, enables the logging of all sql statements generted by sqlalchemy
engine = create_async_engine(DATABASE_URL, echo= True)

#Expire_on_commit = false, prevents session from expiring objects after a commit
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
