from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(ForeignKey("cities.id"), nullable=False, index=True)
    date_time = Column(DateTime, nullable=False, index=True)
    temperature = Column(Float, nullable=False, index=True)
