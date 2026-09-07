from sqlalchemy import select, func
from app.models import Technician, Work_Order, Hospital, OrderStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db, require_role
from app.schemas.technician import SupervisorActiveTechRead, TechnicianCreate, TechnicianCreate, TechnicianRead, TechnicianUpdate
from app.models.enums import UserRole
from app.models.user import User


ACTIVE_STATUSES = [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]

router = APIRouter(prefix = "/technician", tags = ["technician"])


#Get all techs
@router.get("", response_model=list[TechnicianRead])
async def list_technicians(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    statement = select(Technician)
    result = await db.execute(statement)
    return list(result.scalars().all())

#Get tech by id
@router.get("/{technician_id}", response_model=TechnicianRead)
async def get_technician(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    technician = await db.get(Technician, technician_id)
    if technician is None:
        raise HTTPException(
            status_code=404,
            detail=f"Technician {technician_id} not found",
        )
    return technician



@router.get("/active", response_model=list[SupervisorActiveTechRead])
async def get_active_technicians_by_supervisor(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
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

#Create a new technician
@router.post("", response_model=TechnicianRead, status_code=201)
async def create_technician(
    payload: TechnicianCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    technician = Technician(**payload.model_dump())
    db.add(technician)
    await db.commit()
    await db.refresh(technician)
    return technician

#Update a technician
@router.put("/{technician_id}", response_model=TechnicianRead)
async def update_technician(
    technician_id: int,
    payload: TechnicianUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    technician = await db.get(Technician, technician_id)
    if technician is None:
        raise HTTPException(
            status_code=404,
            detail=f"Technician {technician_id} not found",
        )
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(technician, field, value)

    db.add(technician)
    await db.commit()
    await db.refresh(technician)
    return technician

#Delete a technician
@router.delete("/{technician_id}", status_code=204)
async def delete_technician(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    technician = await db.get(Technician, technician_id)
    if technician is None:
        raise HTTPException(
            status_code=404,
            detail=f"Technician {technician_id} not found",
        )
    
    await db.delete(technician)
    await db.commit()
    return None