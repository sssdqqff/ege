from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from backend.app.database import Base
from backend.app.models.user import User

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .attempt import Attempt

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False, default="practice")  #exam, challenge. practice
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(default=None)
    status: Mapped[str] = mapped_column(String, default="in_progress")  #completed, in_progress, abandoned

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="sessions")

    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="session", cascade="all, delete-orphan")