from sqlalchemy import select, func
from app.models import Technician, Work_Order, Hospital, OrderStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.technician import SupervisorActiveTechRead


ACTIVE_STATUSES = [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]

router = APIRouter(prefix = "/technician", tags = ["technician"])

@router.get("/active", response_model=list[SupervisorActiveTechRead])
async def get_active_technicians_by_supervisor(
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(
            Hospital.supervisor_id.label("supervisor_id"),
            func.count(func.distinct(Technician.id)).label("active_technician_count"),
        )
        .join(Technician, Technician.hospital_id == Hospital.id)
        .join(Work_Order, Work_Order.technician_id == Technician.id)
        .where(Work_Order.status.in_(ACTIVE_STATUSES))
        .group_by(Hospital.supervisor_id)
        .order_by(Hospital.supervisor_id)
    )

    result = await db.execute(statement)
    rows = result.all()

    return [
        {
            "supervisor_id": row.supervisor_id,
            "active_technician_count": row.active_technician_count,
        }
        for row in rows
    ]   