from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.routers.base import router as auth_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router)


