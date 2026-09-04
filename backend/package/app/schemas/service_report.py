
from datetime import datetime
 
from pydantic import BaseModel, ConfigDict
 
 
class ServiceReportRead(BaseModel):
    id: int
    work_order_id: int
    file_url: str
    notes: str | None = None
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
 
