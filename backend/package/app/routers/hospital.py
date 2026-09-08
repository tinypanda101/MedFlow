from sqlalchemy import select, func, case
from app.models import Equipment, EquipmentStatus
from app.schemas.hospital import HospitalCreate, HospitalRead, HospitalUpdate, MaintenanceFlagRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db, require_role
from app.models import Hospital
from app.models.enums import UserRole
from app.models.user import User

router = APIRouter(prefix = "/hospitals", tags = ["hospitals"])
#CRUD = need create update delete


#GETS list of hospitals
@router.get("", response_model=list[HospitalRead])
async def list_hospitals(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    #Create statement for DB
    statement = select(Hospital)
    result = await db.execute(statement)

    return list(result.scalars().all())

#GETS equipment flagged for maintenance by hospital
@router.get("/maintenance", response_model=list[MaintenanceFlagRead])
async def get_maintenance_flags(
    db: AsyncSession = Depends(get_db),
    threshold: float = 0.30,
    _: User = Depends(get_current_user),
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

#Create here
@router.post("", response_model=HospitalRead, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    payload: HospitalCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    #converts the payload into a Hospital object using the model_dump method
    hospital = Hospital(**payload.model_dump())
    db.add(hospital)
    await db.commit()
    await db.refresh(hospital)
    return hospital

#Update here
@router.put("/{hospital_id}", response_model=HospitalRead)
async def update_hospital(
    hospital_id: int,
    payload: HospitalUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    hospital = await db.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hospital {hospital_id} not found",
        )

    # exclude_unset=True -> only overwrite fields the client actually sent,
    # so a partial body doesn't null out everything else.
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hospital, field, value)
     
    db.add(hospital)
    await db.commit()
    await db.refresh(hospital)
    return hospital

#Delete here
@router.delete("/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital(
    hospital_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.CLINICAL_ADMIN)),
):
    hospital = await db.get(Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hospital {hospital_id} not found",
        )
    
    await db.delete(hospital)
    await db.commit()
    return None