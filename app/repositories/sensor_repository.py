from sqlalchemy.orm import Session

from app.models.sensor_reading import SensorReading


class SensorRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, reading: SensorReading):

        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)

        return reading

    def get_latest(self):
        return (
            self.db.query(SensorReading)
            .order_by(SensorReading.created_at.desc())
            .first()
        )

    def get_all(self, page: int, limit: int):

        offset = (page - 1) * limit

        return (
            self.db.query(SensorReading)
            .order_by(SensorReading.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_id(self, reading_id: int):

        return (
            self.db.query(SensorReading)
            .filter(SensorReading.id == reading_id)
            .first()
        )

    def delete(self, reading_id: int):

        reading = (
            self.db.query(SensorReading)
            .filter(SensorReading.id == reading_id)
            .first()
        )

        if reading is None:
            return None

        self.db.delete(reading)
        self.db.commit()

        return reading