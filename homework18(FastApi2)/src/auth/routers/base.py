from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="src/templates")

router = APIRouter()

# @router.get("/")
# async def get_root():
#     return {"message": "root route"}

@router.get("/", response_class=HTMLResponse)
def render_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "title": "Auth page"})