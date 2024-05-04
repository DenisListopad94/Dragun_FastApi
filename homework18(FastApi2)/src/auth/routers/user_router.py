from typing import List
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth.routers.helpers import generate_users
from auth.schemas.user_schema import UserCreateSchema, UserIdSchema, UserReadSchema, UserUpdatePartialSchema, UserUpdateSchema
from auth.services.user_service import create_user, create_users, delete_user, delete_users, get_user, get_users, update_partial_user, update_user, update_users
from database import SessionLocal
from sqlalchemy.orm import Session


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


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



@router.post(
    "/create_user",
    response_model=UserReadSchema,
)
def create_user_handler(
        body: UserCreateSchema,
        session: Session = Depends(get_session),
):
    return create_user(
        session=session,
        body=body,
    )

@router.post(
    "/create_users",
    response_model=List[UserReadSchema],
)
def create_users_handler(
        body: List[UserCreateSchema],
        session: Session = Depends(get_session),
):
    return create_users(
        session=session,
        body=body,
    )

@router.get(
    "/get_users",
    response_model=List[UserReadSchema],
)
def get_users_handler(
        session: Session = Depends(get_session),
):
    return get_users(
        session=session,
    )

@router.post(
    "/get_user",
    response_model=UserReadSchema | None
)
def get_user_handler(
        body: UserIdSchema,
        session: Session = Depends(get_session),
):
    return get_user(
        session=session,
        body=body,
    )

@router.put(
    "/update_user",
    response_model=UserReadSchema | None
)
def update_user_handler(
        body: UserUpdateSchema,
        session: Session = Depends(get_session)
):
    return update_user(
        session=session,
        body=body
    )

@router.put(
    "/update_users",
    response_model=List[UserReadSchema]
)
def update_users_handler(
        body: List[UserUpdateSchema],
        session: Session = Depends(get_session)
):
    return update_users(
        session=session,
        body=body
    )

@router.patch(
    "/update_partial_user",
    response_model=UserReadSchema | None
)
def update_partial_user_handler(
        body: UserUpdatePartialSchema,
        session: Session = Depends(get_session)
):
    return update_partial_user(
        session=session,
        body=body
    )


@router.delete(
    "/delete_user/{user_id}",
    response_model=int | None
)
def delete_user_handler(
        user_id: int,
        session: Session = Depends(get_session)
):
    return delete_user(
        session=session,
        user_id=user_id,
    )

@router.delete(
    "/delete_users",
    response_model=int
)
def delete_users_handler(
        user_idx: List[int],
        session: Session = Depends(get_session)
):
    deleted_count = delete_users(
        session=session,
        body=user_idx,
    )
    return deleted_count