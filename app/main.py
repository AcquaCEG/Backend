from fastapi import FastAPI

import app.core.depedencies

from app.api.sensors import router
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    router,
    prefix="/api/sensors",
    tags=["Sensors"]
)

@app.get("/")
def read_root():
    return {"status": "AcquaCEG Backend Online"}