"""
Pydantic Schemas
pip install "fastapi[standard]"
pip freeze > requirements.txt

Schemas are basically used to check incoming payloads and enforce consistency and type-safety
"""

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from app.models import EquipmentStatus

class EquipmentBase(BaseModel):
    serial_number: str = Field(min_length = 1, max_length = 50)
    model: str = Field(min_length = 1, max_length=100)
    charge_level: Decimal = Field(ge = 0, le= 100)
    hospital_id: int
    status: EquipmentStatus = EquipmentStatus.AVAILABLE

#Additional classes can build off what is in EquipmentBase by doing class <name>(EquipmentBase) else they still want (BaseModel)
#Explaining this specific interaction: when creating new equipment we dont give the id (database creates that) but when we want to read that equipment we want the id along with it
class EquipmentCreate(EquipmentBase):
    #Shape of Request Bodyu for POST /Equipment
    None

class EquipmentRead(EquipmentBase):
    #Shape of Equipment in any API response
    id: int
    #model_config acts as control panel that lets us change how data is validated
    #ConfigDict(from_attributes = True) enables ORM (Object relational mapping) mode
    model_config = ConfigDict(from_attributes=True)