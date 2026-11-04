import unittest
from unittest.mock import MagicMock, call, patch

from fastapi import FastAPI
from sqlalchemy import create_engine, inspect

from app import lifespan as lifespan_module
from app.database import database
from app.mqtt import mqtt_service as mqtt_module


class LifespanTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_lifecycle_starts_and_stops_services_once(self):
        from app.main import app

        with (
            patch.object(lifespan_module.mqtt_service, "connect") as mqtt_connect,
            patch.object(lifespan_module.mqtt_service, "disconnect") as mqtt_disconnect,
            patch.object(lifespan_module, "db_connect") as db_connect,
            patch.object(lifespan_module, "db_disconnect") as db_disconnect,
        ):
            async with app.router.lifespan_context(app):
                pass

        mqtt_connect.assert_called_once_with()
        db_connect.assert_called_once_with()
        mqtt_disconnect.assert_called_once_with()
        db_disconnect.assert_called_once_with()

    async def test_database_startup_failure_cleans_both_services_and_preserves_error(self):
        startup_error = RuntimeError("database startup failed")
        with (
            patch.object(lifespan_module.mqtt_service, "connect") as mqtt_connect,
            patch.object(
                lifespan_module.mqtt_service,
                "disconnect",
                side_effect=RuntimeError("mqtt cleanup failed"),
            ) as mqtt_disconnect,
            patch.object(lifespan_module, "db_connect", side_effect=startup_error),
            patch.object(lifespan_module, "db_disconnect") as db_disconnect,
        ):
            with self.assertRaisesRegex(RuntimeError, "database startup failed"):
                async with lifespan_module.lifespan(FastAPI()):
                    self.fail("lifespan yielded after database startup failed")

        mqtt_connect.assert_called_once_with()
        mqtt_disconnect.assert_called_once_with()
        db_disconnect.assert_called_once_with()

    async def test_mqtt_startup_failure_still_attempts_both_cleanups(self):
        with (
            patch.object(
                lifespan_module.mqtt_service,
                "connect",
                side_effect=RuntimeError("mqtt startup failed"),
            ) as mqtt_connect,
            patch.object(lifespan_module.mqtt_service, "disconnect") as mqtt_disconnect,
            patch.object(lifespan_module, "db_connect") as db_connect,
            patch.object(lifespan_module, "db_disconnect") as db_disconnect,
        ):
            with self.assertRaisesRegex(RuntimeError, "mqtt startup failed"):
                async with lifespan_module.lifespan(FastAPI()):
                    self.fail("lifespan yielded after mqtt startup failed")

        mqtt_connect.assert_called_once_with()
        db_connect.assert_not_called()
        mqtt_disconnect.assert_called_once_with()
        db_disconnect.assert_called_once_with()

    async def test_mqtt_cleanup_failure_does_not_skip_database_cleanup(self):
        with (
            patch.object(lifespan_module.mqtt_service, "connect"),
            patch.object(
                lifespan_module.mqtt_service,
                "disconnect",
                side_effect=RuntimeError("mqtt cleanup failed"),
            ) as mqtt_disconnect,
            patch.object(lifespan_module, "db_connect"),
            patch.object(lifespan_module, "db_disconnect") as db_disconnect,
        ):
            with self.assertRaisesRegex(RuntimeError, "mqtt cleanup failed"):
                async with lifespan_module.lifespan(FastAPI()):
                    pass

        mqtt_disconnect.assert_called_once_with()
        db_disconnect.assert_called_once_with()


class RelatedServiceTests(unittest.TestCase):
    def test_dependencies_and_lifespan_share_the_same_mqtt_instance(self):
        from app.core import depedencies

        self.assertIs(depedencies.mqtt_service, mqtt_module.mqtt_service)
        self.assertIs(depedencies.mqtt_service.sensor_service, depedencies.sensor_service)

    def test_database_connect_creates_registered_model_tables_and_disconnect_disposes_engine(self):
        test_engine = create_engine("sqlite:///:memory:")
        with (
            patch.object(database, "engine", test_engine),
            patch.object(test_engine, "dispose", wraps=test_engine.dispose) as dispose,
        ):
            database.connect()
            table_names = inspect(test_engine).get_table_names()
            database.disconnect()

        self.assertIn("sensor_readings", table_names)
        dispose.assert_called_once_with()

    def test_mqtt_connect_starts_async_connection_and_network_loop_once_per_call(self):
        service = mqtt_module.MQTTService.__new__(mqtt_module.MQTTService)
        service.broker = "broker.test"
        service.port = 8883
        service.client = MagicMock()

        service.connect()

        service.client.connect_async.assert_called_once_with(
            "broker.test", 8883, keepalive=60
        )
        service.client.loop_start.assert_called_once_with()

    def test_mqtt_disconnect_stops_loop_and_disconnects_client(self):
        service = mqtt_module.MQTTService.__new__(mqtt_module.MQTTService)
        service.client = MagicMock()

        service.disconnect()

        self.assertEqual(
            service.client.method_calls,
            [call.loop_stop(), call.disconnect()],
        )


if __name__ == "__main__":
    unittest.main()
