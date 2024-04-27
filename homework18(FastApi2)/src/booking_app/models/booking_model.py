from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from auth.models.user_model import User
from src.core.models import Base
from src.core.models.base import (
    created_at,
    updated_at,
    str_300,
    datetime_column,
)


class PaymentStatus(str, Enum):
    Waiting_execution = "Waiting_execution"
    Confirmed = "Confirmed"
    Canceled = "Canceled"

class Booking(Base):
    confirmation_id: Mapped[UUID] = mapped_column(default=uuid4, nullable=True)
    description: Mapped[str_300] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    payment_status: Mapped[PaymentStatus] = mapped_column(nullable=True)
    payment_time: Mapped[datetime_column] = mapped_column(nullable=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="booking")