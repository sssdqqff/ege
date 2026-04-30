from sqlalchemy import Integer, String, Column, func, ForeignKey
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
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    difficulty: Mapped[str] = mapped_column(String, default="medium")  # easy, medium, hard

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False, ondelete="CASCADE")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="topic", cascade="all, delete-orphan")