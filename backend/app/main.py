from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.api.routes import router
from app.db import Base, engine

# Explicit path to .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Backend is working"}