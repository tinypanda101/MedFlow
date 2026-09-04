from pydantic import BaseModel, ConfigDict

class MaintenanceFlagRead(BaseModel):
    hospital_id: int
    hospital_name: str
    total_equipment: int
    flagged: int
    flagged_ratio: float
    model_config = ConfigDict(from_attributes=True)
