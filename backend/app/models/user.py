from sqlalchemy import Integer, String, Column, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .attempt import Attempt
    from .session import Session

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)

    avatar_url: Mapped[str] = mapped_column(String, nullable=True)

    xp: Mapped[int] = mapped_column(default=0, index=True)
    level: Mapped[int] = mapped_column(default=1, index=True)
    last_login: Mapped[datetime] = mapped_column(nullable=True)
    streak: Mapped[int] = mapped_column(default=0)

    role: Mapped[str] = mapped_column(String, default="user")

    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user", cascade="all, delete-orphan")