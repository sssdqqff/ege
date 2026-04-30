from sqlalchemy import Integer, String, Column, Text, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .topic import Topic
    from .attempt import Attempt
    from .subject import Subject

from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    condition: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    answer_type: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String, default="medium")  # easy, medium, hard
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False, ondelete="CASCADE")
    topic: Mapped["Topic"] = relationship("Topic", back_populates="tasks")
    
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False, ondelete="CASCADE")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="tasks")

    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="task", cascade="all, delete-orphan")