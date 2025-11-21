from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.session import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


organisation_activity = Table(
    'organisation_activity',
    Base.metadata,
    Column('organisation_id', Integer, ForeignKey('organisation.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activity.id'), primary_key=True)
)


class Organisation(BaseModel):
    __tablename__ = "organisation"

    title = Column(String(255), unique=True)
    phone = Column(String(255), unique=True)
    building: Mapped[list["Building"]] = relationship("Building", back_populates="organisation")
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organisation_activity,
        back_populates="organisations"
    )


class Building(BaseModel):
    __tablename__ = "building"

    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    organisation: Mapped[Organisation] = relationship("Organisation", back_populates="building")


class Activity(BaseModel):
    __tablename__ = "activity"

    title = Column(String(255), unique=True)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("activity.id"))
    children = relationship("Activity")

    organisations: Mapped[list["Organisation"]] = relationship(
        "Organisation",
        secondary=organisation_activity,
        back_populates="activities"
    )
