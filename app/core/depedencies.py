from app.database.database import SessionLocal
from app.repositories.sensor_repository import SensorRepository
from app.services.sensor_service import SensorService
from app.mqtt.mqtt_service import MQTTService

sensor_service = SensorService(SessionLocal)
mqtt_service = MQTTService()

mqtt_service.set_sensor_service(sensor_service)
try:
    mqtt_service.connect()
    print("MQTT conectado.")
except Exception as e:
    print(f"MQTT indisponível: {e}")