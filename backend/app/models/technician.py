""""
Technician Model to help answer some of the questions espeically #2
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .hospital import Hospital
    from .work_order import Work_Order

class Technician(Base):
    __tablename__= "technicians"

    #need id, name, facility_id

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))

    #foreign key
    hospital_id: Mapped[int] = mapped_column(Integer, ForeignKey("hospitals.id"))

    #relationships
    hospital: Mapped["Hospital"] = relationship(back_populates="technicians")
    work_order: Mapped["Work_Order"] = relationship(back_populates="technician")

    def __repr__(self) -> str:
        return (f"Technician(id={self.id}, name={self.name!r}, hospital_id={self.hospital_id})")
