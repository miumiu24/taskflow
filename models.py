from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    # Связь "Один ко многим"
    # Один пользователь может иметь много задач
    tasks = relationship("Task", back_populates="author")

# Создаем класс-чертеж для наших задач
class Task(Base):
    __tablename__ = "tasks"  # 1. Имя таблицы в самой базе данных

    # 2. Описываем колонки (атрибуты класса)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Внешний ключ: к какому пользователю привязана задача
    user_id = Column(Integer, ForeignKey("users.id"))

    # Обратная связь
    author = relationship("User", back_populates="tasks")

