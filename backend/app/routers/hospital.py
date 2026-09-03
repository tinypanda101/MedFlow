from sqlalchemy import select, func, case
from app.models import Equipment, EquipmentStatus
from app.schemas.hospital import MaintenanceFlagRead
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models import Hospital

router = APIRouter(prefix = "/hospitals", tags = ["hospitals"])


@router.get("/maintenance", response_model=list[MaintenanceFlagRead])
async def get_maintenance_flags(
    db: AsyncSession = Depends(get_db),
    threshold: float = 0.30,
):
    flagged = func.count(
        case((Equipment.status == EquipmentStatus.MAINTENANCE, Equipment.id))
    )
    total = func.count(Equipment.id)

    statement = (
        select(
            Equipment.hospital_id.label("hospital_id"),
            Hospital.name.label("hospital_name"),
            total.label("total_equipment"),
            flagged.label("flagged"),
        )
        .join(Hospital, Hospital.id == Equipment.hospital_id)
        .group_by(Equipment.hospital_id, Hospital.name)
        .order_by(Equipment.hospital_id)
    )

    result = await db.execute(statement)
    rows = result.all()

    return [
        {
            "hospital_id": row.hospital_id,
            "hospital_name": row.hospital_name,
            "total_equipment": row.total_equipment,
            "flagged": row.flagged,
            "flagged_ratio": row.flagged / row.total_equipment,
        }
        for row in rows
    ]