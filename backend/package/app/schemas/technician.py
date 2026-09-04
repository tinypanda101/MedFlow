from pydantic import BaseModel, ConfigDict

class SupervisorActiveTechRead(BaseModel):
    supervisor_id: int
    active_technician_count: int
    model_config = ConfigDict(from_attributes=True)