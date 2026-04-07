from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv
import os

# Explicit path to .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Backend is working"}