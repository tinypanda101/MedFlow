"""
    Co-Location Discrepancies
"""

from pydantic import Field

from pydantic import BaseModel, ConfigDict

from app.models import OrderPriority, OrderStatus


class DiscrepancyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    work_order_id: int
    title: str
    equipment_hospital_id: int
    technician_hospital_id: int

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderRead(BaseModel):
    id: int
    title: str
    priority: OrderPriority
    status: OrderStatus
    equipment_id: int
    technician_id: int
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    priority: OrderPriority
    equipment_id: int
    technician_id: int
    # status intentionally omitted - model defaults to PENDING.
    model_config = ConfigDict(from_attributes=True)


class ModelRatioRead(BaseModel):
    model: str
    total: int
    completed: int
    failed: int
    pending: int
    completion_ratio: float | None # completed / completed+failed
    failure_ratio: float | None # failed / completed+failed
    model_config = ConfigDict(from_attributes=True)