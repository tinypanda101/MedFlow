"""
Seeds demo users for RBAC
"""

import asyncio

from app.database import AsyncSessionLocal
from app.models import User, UserRole
from app.security import hash_password

async def seed_users() -> None:
    async with AsyncSessionLocal() as session:
        session.add_all([
            User(
                username="admin",
                role=UserRole.CLINICAL_ADMIN,
                hashed_password=hash_password("adminpass"),
            ),
            User(
                username="technician",
                role=UserRole.FIELD_TECHNICIAN,
                hashed_password=hash_password("technicianpass"),
            ),
            User(
                username="auditor",
                role=UserRole.AUDITOR,
                hashed_password=hash_password("auditorpass"),
            )
        ])
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_users())