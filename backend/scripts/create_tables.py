"""
Script that makes the tables and enum types

run this from \backend directory with .venv enabled:
    python -m scripts.create_tables
"""

import asyncio

from app.database import engine

from app.models import Base

async def create_tables() -> None:
    async with engine.begin() as conn:
        #Create_all() method provided by SQLAlchemy that creates all tables in metadata
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())