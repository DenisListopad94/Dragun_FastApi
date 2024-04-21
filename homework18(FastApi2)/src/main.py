from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from auth.routers import base, user_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(base.router, prefix="/auth")
app.include_router(user_router.router, prefix="/auth")

