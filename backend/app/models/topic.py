from sqlalchemy import Integer, String, func, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .subject import Subject
    from .task import Task

from ..database import Base

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    difficulty: Mapped[str] = mapped_column(String, default="medium")  # easy, medium, hard

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="topic", cascade="all, delete-orphan")