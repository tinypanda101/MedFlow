"""
Equipment Model - Skipping plain python version to jump into the SQLAlchemy ORM(object relational mapping) version
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from app.models import EquipmentStatus

if TYPE_CHECKING:
    from .hospital import Hospital
    from .work_order import Work_Order

class Equipment(Base):
    __tablename__ = "equipment"

    #equipment has id, serial_number, model, status, charge_level, facility_id

    #Table level constraint for charge_level 0-100
    __table_args__ = (CheckConstraint("charge_level BETWEEN 0 and 100", name = "charge_level_range"),)

    #Columns
    id: Mapped[int] = mapped_column(primary_key = True)
    serial_number: Mapped[str] = mapped_column(String(50), unique= True)
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[EquipmentStatus] = mapped_column(SQLEnum(
        EquipmentStatus, name = "equipment_status",
        #definition for how enum values are stored in the database, we are using string representation of enum members
        values_callable = lambda enum_cls: [member.value for member in enum_cls],
    ), default= EquipmentStatus.AVAILABLE)
    charge_level: Mapped[Decimal] = mapped_column(Numeric(5,2))
    hospital_id: Mapped[int] = mapped_column(Integer, ForeignKey("hospitals.id"))

    #Do relationships here
    hospital: Mapped["Hospital"] = relationship(back_populates="equipments")
    work_order: Mapped["Work_Order"] = relationship(back_populates="equipments")
    #Future methods go here


    #__repr__ here
    def __repr__(self) -> str:                                                                                  #Remember Enum = .value
        return (f"Equipment(Serial = {self.serial_number!r}, Model = {self.model!r}, Charge = {self.charge_level}, Status = {self.status.value})")
 