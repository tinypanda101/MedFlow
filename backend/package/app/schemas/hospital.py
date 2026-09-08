from pydantic import BaseModel, ConfigDict

class HospitalRead(BaseModel):
    id: int
    name: str
    location_region: str
    capacity: int
    supervisor_id: int
    model_config = ConfigDict(from_attributes=True)

class HospitalCreate(BaseModel):
    name: str
    location_region: str
    capacity: int
    supervisor_id: int

class HospitalUpdate(BaseModel):
    name: str | None = None
    location_region: str | None = None
    capacity: int | None = None
    supervisor_id: int | None = None
    model_config = ConfigDict(from_attributes=True)

class MaintenanceFlagRead(BaseModel):
    hospital_id: int
    hospital_name: str
    total_equipment: int
    flagged: int
    flagged_ratio: float
    model_config = ConfigDict(from_attributes=True)
