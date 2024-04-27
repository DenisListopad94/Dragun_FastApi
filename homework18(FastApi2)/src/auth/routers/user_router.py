from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth.routers.helpers import generate_users


router = APIRouter(
    prefix="/users",
    tags=["Auth"]
)

templates = Jinja2Templates(directory="src/templates")


# @router.get("/users/")
# async def get_users():
#     return {"message": "users route"}

@router.get("/", response_class=HTMLResponse)
def render_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "title": "Users page", "users": generate_users(10)})

