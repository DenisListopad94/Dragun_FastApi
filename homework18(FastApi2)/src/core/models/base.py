import datetime
from typing import Annotated
from sqlalchemy import (
    String,
    text,
    DateTime
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

str_30 = Annotated[str, mapped_column(String(30))]
str_300 = Annotated[str, mapped_column(String(300))]
datetime_column = Annotated[datetime.datetime, mapped_column(DateTime)]

class Base(DeclarativeBase):
    __abstract__ = True
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)