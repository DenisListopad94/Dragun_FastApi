from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.auth.routers.user_router import router as user_router

templates = Jinja2Templates(directory="src/templates")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# @router.get("/")
# async def get_root():
#     return {"message": "root route"}

@router.get("/", response_class=HTMLResponse)
def render_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "title": "Auth page"})


router.include_router(user_router)