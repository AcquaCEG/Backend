import json
import logging

import paho.mqtt.client as mqtt
from pydantic import ValidationError

from app.core.config import MQTT_TOPIC, MQTT_PORT, MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID
from app.schemas.sensor import SensorReadingIn

logger = logging.getLogger(__name__)

class MQTTService:

    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT):
        self.broker = broker
        self.port = port
        self.latest_data = {}
        self.sensor_service = None

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=MQTT_CLIENT_ID
        )

        self.client.username_pw_set(
            MQTT_USERNAME,
            MQTT_PASSWORD
        )

        self.client.tls_set(ca_certs="app/certs/emqxsl-ca.crt")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def set_sensor_service(self, sensor_service):
        self.sensor_service = sensor_service

    def connect(self):
        self.client.connect_async(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("Conectado ao broker MQTT")
            client.subscribe(
                MQTT_TOPIC,
                qos=1
            )
        else:
            logger.error(
                "Falha ao conectar ao broker MQTT: %s (%s)",
                reason_code,
                reason_code.getName(),
            )

    def on_message(self, client, userdata, msg):
        try:
            raw_data = json.loads(msg.payload.decode())
            data = SensorReadingIn.model_validate(raw_data)
            validated_data = data.model_dump()

            self.latest_data = validated_data
            logger.info("Leitura MQTT validada: topic=%s dados=%s", msg.topic, validated_data)

            if self.sensor_service:
                self.sensor_service.save_reading(validated_data)

        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logger.warning("Payload MQTT não contém JSON válido: topic=%s erro=%s", msg.topic, e)
        except ValidationError as e:
            logger.warning(
                "Leitura MQTT rejeitada por dados inválidos: topic=%s erros=%s",
                msg.topic,
                e.errors(),
            )
        except Exception as e:
            logger.exception("Erro ao processar mensagem MQTT: topic=%s erro=%s", msg.topic, e)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
