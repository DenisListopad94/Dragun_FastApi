from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from auth.models.user_model import UserRole


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    role: UserRole


class UserCreateSchema(UserBaseSchema):
    pass

class UserReadSchema(UserBaseSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: int

class UserIdSchema(BaseModel):
    id: int

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    role: UserRole
    id: int
    # updated_at: Optional[datetime]

class UserUpdatePartialSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole | None = None
    id: int