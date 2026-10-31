from fastapi import APIRouter, HTTPException, Query

from app.schemas.sensor import SensorData, SensorReadingOut
from app.core.depedencies import sensor_service

router = APIRouter()

@router.get("/latest", response_model=SensorData)
def read_latest():

    reading = sensor_service.get_latest()

    if reading is None:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma leitura encontrada."
        )

    return reading

@router.get("/readings", response_model=list[SensorReadingOut])
def all_reads(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500)
):

    return sensor_service.get_all(page, limit)

@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int):

    reading = sensor_service.get_by_id(reading_id)

    if reading is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return reading

@router.delete("/readings/{reading_id}")
def delete_reading(reading_id: int):

    deleted = sensor_service.delete_reading(reading_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Leitura não encontrada."
        )

    return {"message": "Leitura removida com sucesso."}