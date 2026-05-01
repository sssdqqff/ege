from sqlalchemy import Integer, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .topic import Topic
    from .task import Task

from ..database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")