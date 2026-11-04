from contextlib import asynccontextmanager
import sys

from fastapi import FastAPI

from app.database.database import connect as db_connect, disconnect as db_disconnect
from app.mqtt.mqtt_service import mqtt_service

import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Inicializando serviços do AcquaCEG...")

        db_connect()
        logger.info("Inicializando Banco de Dados...")
        
        mqtt_service.connect()
        logger.info("Inicializando MQTT...")

        logger.info("Aplicação pronta para receber requisições.")
        yield
    finally:
        logger.info("Encerrando serviços da aplicação...")

        startup_or_runtime_failed = sys.exc_info()[0] is not None
        cleanup_errors = []

        for cleanup, success_message, service_name in (
            (mqtt_service.disconnect, "Cliente MQTT desconectado.", "MQTT"),
            (db_disconnect, "Banco de dados encerrado.", "banco de dados"),
        ):
            try:
                cleanup()
                logger.info(success_message)
            except Exception:
                cleanup_errors.append(sys.exc_info()[1])
                logger.exception("Falha ao encerrar o serviço de %s.", service_name)

        if cleanup_errors:
            logger.error("Aplicação encerrada com falhas durante o cleanup.")
        else:
            logger.info("Aplicação encerrada com sucesso.")

        if cleanup_errors and not startup_or_runtime_failed:
            raise cleanup_errors[0]
