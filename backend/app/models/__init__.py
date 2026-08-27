"""
Lets me write app.models import instead of app.models.hospital/equipment
"""
from .base import Base
from .enums import EquipmentStatus, OrderPriority, OrderStatus, UserRole
from .equipment import Equipment
from .hospital import Hospital
from .work_order import Work_Order
from .technician import Technician
from .service_report import Service_Report
#others as well

__all__ = [
    "Base",
    "EquipmentStatus",
    "OrderPriority",
    "OrderStatus",
    "UserRole",
    "Equipment",
    "Hospital",
    "Service_Report",
    "Work_Order",

]