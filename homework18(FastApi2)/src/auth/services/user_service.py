from typing import List
from sqlalchemy.orm import Session

from auth.models.user_model import User
from auth.schemas.user_schema import UserCreateSchema, UserIdSchema, UserReadSchema, UserUpdatePartialSchema, UserUpdateSchema


def create_user(
        session: Session,
        body: UserCreateSchema
) -> User:
    user = User(
        first_name=body.first_name,
        last_name=body.last_name,
        role=body.role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(
        session: Session,
        body: UserIdSchema
) -> User | None:
    return session.query(User).filter(User.id == body.id).first()

def get_users(
        session: Session,
) -> List[User]:
    return session.query(User).all()

def update_user(
        session: Session,
        body: UserUpdateSchema
) -> User | None:
    user = session.query(User).filter(User.id == body.id).first()

    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.role = body.role

        session.commit()
        session.refresh(user)
        return user
    else:
        return None
    
def update_partial_user(
        session: Session,
        body: UserUpdatePartialSchema
) -> User | None:
    user = session.query(User).filter(User.id == body.id).first()

    if user:
        if body.first_name is not None:
            user.first_name = body.first_name
        if body.last_name is not None:
            user.last_name = body.last_name
        if body.role is not None:
            user.role = body.role

        session.commit()
        session.refresh(user)
        return user
    else:
        return None


def delete_user(
    session: Session,
    user_id: int,
):
    user = session.query(User).filter(User.id == user_id).first()
    if user: 
        session.delete(user)
        session.commit()
        return user_id
    else: return None


def create_users(session: Session, body: List[UserCreateSchema]) -> List[User]:
    created_users = []
    for user_data in body:
        user = User(**user_data.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        created_users.append(user)
    return created_users

def update_users(session: Session, body: List[UserUpdateSchema]) -> List[User]:
    updated_users = []
    for user_data in body:
        user = session.query(User).filter(User.id == user_data.id).first()
        if user:
            for field, value in user_data:
                setattr(user, field, value)
            session.commit()
            session.refresh(user)
            updated_users.append(user)
    return updated_users


def delete_users(session: Session, body: list[int]) -> int:
    deleted_count = 0
    for user_id in body:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            deleted_count += 1
    return deleted_count