import logging

from app.database.database import SessionLocal
from app.repositories.sensor_repository import SensorRepository
from app.services.sensor_service import SensorService
from app.mqtt.mqtt_service import MQTTService

logger = logging.getLogger(__name__)

sensor_service = SensorService(SessionLocal)
mqtt_service = MQTTService()

mqtt_service.set_sensor_service(sensor_service)
try:
    mqtt_service.connect()
    logger.info("Cliente MQTT iniciado; aguardando conexão com o broker")
except Exception as e:
    logger.exception("Não foi possível iniciar o cliente MQTT: %s", e)
