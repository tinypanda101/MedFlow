"""
Lets me write app.models import instead of app.models.hospital/equipment
"""

from .enums import EquipmentStatus, OrderPriority, OrderStatus, UserRole
from .equipment import Equipment
from .hospital import Hospital
from .base import Base
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