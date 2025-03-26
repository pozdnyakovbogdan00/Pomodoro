from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class Task(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=False)

class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]