"""
Hospital Model - Skipping plain python version to jump into the SQLAlchemy ORM(object relational mapping) version
"""

# Makes every type annotation in the file a plain, unevaluated string at class def time
from __future__ import annotations

# Constant that is always false at run-time avoids circular imports
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship



from .base import Base

if TYPE_CHECKING:
    from .equipment import Equipment
    from .technician import Technician

#requries base from .base. Why? idk something to do with the ORM workings
class Hospital(Base):
    #Sets the table name for hospital model in the database proper
    __tablename__ = "hospitals"

    #Defines the attributes in hospitals
    #id, name, location_region, capacity, supervisor_id || No foreign key in this one afaik
    #RoboPulse example: id: Mapped[int] = mapped_column(primary_key = True)
    #RoboPulse example: location_region: Mapped[str] = mapped_column(String(50))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100)) #str = python, String = SQLAlchemy
    location_region: Mapped[str] = mapped_column(String(50)) #Just copying the char limits over from RoboPulse I don't believe theres a set limit in Medflow
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)
    #Mapped[int/str/etc] is hinting to python that its that specific var type
    #mapped_column() is what the database makes the column

    #Creates the relationships with other tables
    #Will come back when others are created but this connects to equipment and maybe a technician table
    #Use list if for instance here hospital has multiple equipment (ie list = one of one=to=many)
    #Whichever side is the ForeignKey side is the Many side which points to "one" parent
    #Mapped[Equipment] must match Equipment(class name in equipment.py)
    #back_populates="hospital" must match the hospital: Mapped... on Equipment.py
    equipments: Mapped[list["Equipment"]] = relationship(back_populates="hospital")
    technicians: Mapped[list["Technician"]] = relationship(back_populates="hospital")

    #its a ToString method but I am unsure the purpose of it?
    def __repr__(self) -> str:
        return (f"Hospital(id = {self.id}, name = {self.name!r}, region = {self.location_region!r})")
        #!r just makes it a literal (ie no random @ /n etc will break it)