from sqlalchemy import Integer, String, Column, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .topic import Topic

from ..database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")