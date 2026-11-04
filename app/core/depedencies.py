import logging

from app.database.database import SessionLocal
from app.repositories.sensor_repository import SensorRepository
from app.services.sensor_service import SensorService
from app.mqtt.mqtt_service import mqtt_service

logger = logging.getLogger(__name__)

sensor_service = SensorService(SessionLocal)
mqtt_service.set_sensor_service(sensor_service)