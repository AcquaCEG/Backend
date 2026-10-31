from app.schemas.sensor import SensorData, SensorReadingOut
from app.models.sensor_reading import SensorReading
from app.repositories.sensor_repository import SensorRepository


class SensorService:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    # ---------- conversões ----------

    def convert_temperature(self, temperature):
        # Futuramente: ADC -> °C
        return temperature

    def convert_ph(self, ph):
        # Futuramente:
        # m = ...
        # b = ...
        # return m * adc + b
        return ph

    def convert_condut(self, conductivity):
        # Futuramente:
        # m = ...
        # b = ...
        # return m * adc + b
        return conductivity

    def convert_water_level(self, water_level):
        return bool(water_level)

    def _convert_raw_data(self, raw_data):

        raw_temperature = raw_data["temperature"]
        raw_ph = raw_data["adc_ph"]
        raw_conductivity = raw_data["adc_condut"]
        raw_water_level = raw_data["water_level"]

        temperature = self.convert_temperature(raw_temperature)
        ph = self.convert_ph(raw_ph)
        conductivity = self.convert_condut(raw_conductivity)
        water_level = self.convert_water_level(raw_water_level)

        return temperature, ph, conductivity, water_level

    # ---------- conversão ORM -> schema ----------

    def _to_schema(self, reading: SensorReading) -> SensorData:
        return SensorData(
            temperature=reading.temperature,
            ph=reading.ph,
            conductivity=reading.conductivity,
            waterLevel=reading.water_level
        )

    def _to_out(self, reading: SensorReading) -> SensorReadingOut:
        return SensorReadingOut.model_validate(reading)

    # ---------- operações ----------

    def save_reading(self, raw_data):

        temperature, ph, conductivity, water_level = self._convert_raw_data(raw_data)

        reading = SensorReading(
            ph=ph,
            conductivity=conductivity,
            temperature=temperature,
            water_level=water_level
        )

        with self.session_factory() as db:
            return SensorRepository(db).save(reading)

    def get_latest(self):

        with self.session_factory() as db:
            reading = SensorRepository(db).get_latest()

            if reading is None:
                return None

            return self._to_schema(reading)

    def get_all(self, page: int, limit: int):

        with self.session_factory() as db:
            readings = SensorRepository(db).get_all(page, limit)

            return [self._to_out(r) for r in readings]

    def get_by_id(self, reading_id: int):

        with self.session_factory() as db:
            reading = SensorRepository(db).get_by_id(reading_id)

            if reading is None:
                return None

            return self._to_out(reading)

    def delete_reading(self, reading_id: int):

        with self.session_factory() as db:
            return SensorRepository(db).delete(reading_id)