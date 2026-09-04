"""
Service Report Model
"""

from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .work_order import Work_Order

class Service_Report(Base):
    __tablename__ = "service_report"

    id: Mapped[int] = mapped_column(primary_key=True)
    #need mission id
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("work_orders.id"))
    file_url: Mapped[str] = mapped_column(Text)
    #Make it option add | None and nullable
    notes: Mapped[str | None] = mapped_column(Text, nullable = True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default= func.now())

    #relationships
    work_order: Mapped["Work_Order"] = relationship(back_populates="service_reports")

    def __repr__(self) -> str:
        return (f"Service Report(id = {self.id}, work order id = {self.work_order_id}, file_url = {self.file_url!r})")