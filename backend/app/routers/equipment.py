"""
Routers = Endpoints

At this point we have everything we need to expose our applicatoin to the internet we just need to define how the endpoints are created.

we'll need to give the endpoints a URL (everything here should be under /equipment) and then define any additional parameters as needed

Common pattern for REST endpoints:
GET /equipment -> Gets all equipment
GET /equipment/1 -> Get equipment with id = 1
POST /equipment-> Creates a equipment resource
PUT /equipment/2 -> Updates equipment with id=2
DELETE /equipment/3 -> Delete equipment with id=3

Query parameter (This is getting replaced with the new http method):
GET /equipment?max_charge=20 -> gets all equipment where max battery is 20
"""


from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EquipmentStatus # User, UserRole #user/userrole are for RBAC later
from app.schemas.equipment import EquipmentCreate, EquipmentRead
from app.dependencies import get_db # get_current_user, require_role #get_current and require are also RBAC later
from app.models import Equipment

#Every request comes under /equipment
router = APIRouter(prefix = "/equipment", tags = ["equipment"])

#This decorator says this goes to "/equipment" with nothing else and returns a list of EquipmentRead objects
@router.get("", response_model= list[EquipmentRead])
async def list_equipment(max_charge: Decimal | None = Query(default = None, ge=0, le=100, description="Only return equipment below this charge level"),
                         db: AsyncSession = Depends(get_db)): #add RBAC here
    #Need to be able to interact with DB so we need session object to execute those statements
    #Dependent on the session object

    #Create statement for DB
    statement = select(Equipment).where(Equipment.status != EquipmentStatus.OFFLINE)

    #check for charge query
    if max_charge is not None:
        statement = statement.where(Equipment.charge_level < max_charge)

    result = await db.execute(statement)

    #scalars() basically makes it cleaner than a bulky database query result
    return list(result.scalars().all())

#Gets specific equipment by its id
#GET /equipment/{equipment_id} is known as a PATH PARAMETER
@router.get("/{equipment_id}", response_model= EquipmentRead)
async def get_equipment(equipment_id: int, db:AsyncSession = Depends(get_db)): #RBAC add remember
    equipment = await db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Equipment {equipment_id} not found"
        )
    return equipment

#POST requests are used for creating new resources or altering state
@router.post("", response_model= EquipmentRead, status_code=status.HTTP_201_CREATED)
async def create_equipment(payload: EquipmentCreate, db: AsyncSession = Depends(get_db)): #Remember RBAC later
    # ** converts a dict of data into invidivual arugments (ie very important)
    equipment = Equipment(**payload.model_dump())

    db.add(Equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment



#for every new endpoint put either _: User = Depends(get_current_user) or if you want only specific roles _:User = Depends(require_role(UserRole.<Role>))