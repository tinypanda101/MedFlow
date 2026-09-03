"""
    Co-Location Discrepancies
"""

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
    operator_id: int
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