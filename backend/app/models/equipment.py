"""
Equipment Model - Skipping plain python version to jump into the SQLAlchemy ORM(object relational mapping) version
"""



from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    #equipment has id, serial_number, model, status, charge_level, facility_id

    #Table level constraint for charge_level 0-100
    __table_args__ = (CheckConstraint("Battery_level BETWEEN 0 and 100", name = "charge_level_range"),)

    #Columns
    id: Mapped[int] = mapped_column(primary_key = True)
    serial_number: Mapped[str] = mapped_column(String(50), unique= True)
    model: Mapped[str] = mapped_column(String(100))
    #status is an enum need to set that up
    charge_level: Mapped[Decimal] = mapped_column(Numeric(5,2))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("hospitals.id"))

    #Do relationships here



    #__repr__ here
 