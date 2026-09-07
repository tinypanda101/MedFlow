from pydantic import BaseModel, ConfigDict

class SupervisorActiveTechRead(BaseModel):
    supervisor_id: int
    active_technician_count: int
    model_config = ConfigDict(from_attributes=True)

class TechnicianRead(BaseModel):
    id: int
    name: str
    hospital_id: int
    model_config = ConfigDict(from_attributes=True)

class TechnicianCreate(BaseModel):
    name: str
    hospital_id: int

class TechnicianUpdate(BaseModel):
    name: str | None = None
    hospital_id: int | None = None
    model_config = ConfigDict(from_attributes=True)