from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorData(BaseModel):
    temperature: float
    ph: float
    conductivity: int
    waterLevel: bool


class SensorReadingOut(BaseModel):
    # from_attributes permite criar o schema direto de um objeto ORM:
    # SensorReadingOut.model_validate(reading)
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    temperature: float | None
    ph: float
    conductivity: int
    # lê de reading.water_level, mas serializa como "waterLevel"
    # para manter o mesmo nome que a API já usa em /latest
    water_level: bool = Field(serialization_alias="waterLevel")