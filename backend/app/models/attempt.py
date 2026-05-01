from sqlalchemy import Boolean, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .task import Task
    from .session import Session

from ..database import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_answer: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship("Task", back_populates="attempts")
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="attempts")

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    session: Mapped["Session"] = relationship("Session", back_populates="attempts")