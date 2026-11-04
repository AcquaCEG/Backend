from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def connect():
    # Import the model here so its table is registered in Base.metadata before
    # create_all runs, without introducing a database/model import cycle.
    import app.models.sensor_reading

    Base.metadata.create_all(bind=engine)

def disconnect():
    engine.dispose()
