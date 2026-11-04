import logging

from fastapi import FastAPI
from app.lifespan import lifespan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

import app.core.depedencies

from app.api.sensors import router

app = FastAPI(lifespan=lifespan)

app.include_router(
    router,
    prefix="/api/sensors",
    tags=["Sensors"]
)

@app.get("/")
def read_root():
    return {"status": "AcquaCEG Backend Online"}
