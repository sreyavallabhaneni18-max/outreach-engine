from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.api.routes import router
from app.db import Base, engine
from app.api.webhooks import router as webhook_router


# Explicit path to .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(webhook_router)


@app.get("/")
def home():
    return {"message": "Backend is working"}