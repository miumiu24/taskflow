from enum import Enum
from pydantic import ConfigDict, BaseModel, Field, computed_field
from datetime import datetime
from typing import Optional

# 1. Создаем наш список разрешенных статусов
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

# 2. Создаем схему по ТЗ
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50, description="Название задачи")
    description: Optional[str] = Field(default="", description="Описание задачи")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Статус задачи")
    user_id: int = Field(description="ID пользователя-автора")

# Схема для отображения задачи (то, что сервер возвращает пользователю)
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool  # Это есть в базе

    # Добавляем вычисляемое поле для статуса, чтобы API отдавало его красиво
    @computed_field
    @property
    def status(self) -> TaskStatus:
        return TaskStatus.DONE if self.is_completed else TaskStatus.TODO