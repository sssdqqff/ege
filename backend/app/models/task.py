from sqlalchemy import Integer, String, Column, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    condition: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    answer_type: Mapped[str] = mapped_column(String)
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_id: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, default="medium")  # easy, medium, hard
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())