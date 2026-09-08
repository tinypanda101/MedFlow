"""
Work_Order model 
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import OrderStatus, OrderPriority

if TYPE_CHECKING:
    from .service_report import Service_Report
    from .technician import Technician
    from .equipment import Equipment

class Work_Order(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    priority: Mapped[OrderPriority] = mapped_column(SQLEnum(
        OrderPriority,
        name = "order_priority",
        values_callable = lambda enum_cls: [member.value for member in enum_cls],
        )
    )
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(
      OrderStatus,
      name = "order_status",
      values_callable = lambda enum_cls: [member.value for member in enum_cls],  
        ),
        default= OrderStatus.PENDING,
    )
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipment.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))


    #relationships here
    
    equipment: Mapped["Equipment"] = relationship(back_populates="work_orders")
    technician: Mapped["Technician"] = relationship(back_populates="work_orders")
    service_reports: Mapped[list["Service_Report"]] = relationship(back_populates="work_order")

    def mark_completed(self) -> None:
        self.status = OrderStatus.COMPLETED

    def mark_failed(self) -> None:
        self.status = OrderStatus.FAILED


    def __repr__(self) -> str:
        return (f"Work Order(id = {self.id}, title = {self.title!r}, priority = {self.priority.value}, status = {self.status.value} )")