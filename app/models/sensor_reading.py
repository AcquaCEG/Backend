from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer

from app.database.database import Base

class SensorReading(Base):

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ph = Column(Float, nullable=False)
    conductivity = Column(Integer, nullable=False)
    temperature = Column(Float)
    water_level = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, ph, conductivity, temperature, water_level):
        self.ph = ph
        self.conductivity = conductivity
        self.temperature = temperature
        self.water_level = water_level