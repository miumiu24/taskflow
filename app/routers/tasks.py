from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from sqlalchemy.orm import joinedload

from database import SessionLocal
from models import Task
from app.schemas.tasks import TaskCreate, TaskResponse, TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# АсинCustomный генератор сессий базы данных
async def get_db():
    async with SessionLocal() as db:  # Конструкция async with сама закроет сессию в конце!
        yield db


# 1. Асинхронное создание задачи
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):

    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        is_completed=(task.status == TaskStatus.DONE)
    )

    db.add(db_task)

    await db.commit()
    await db.refresh(db_task)

    return db_task


# 2. Асинхронное получение всех задач
@router.get("", response_model=List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    # В асинхронной Алхимии запросы делаются через функцию select()
    query = select(Task)
    result = await db.execute(query)

    # Достаем чистые объекты из результата запроса
    tasks = result.scalars().all()
    return tasks


@router.get("/with-authors-optimized")
async def get_tasks_with_authors_good(db: AsyncSession = Depends(get_db)):
    # 1. Мы сразу говорим базе: "Принеси задачи ВМЕСТЕ с их авторами"
    query = select(Task).options(joinedload(Task.author))

    # 2. Выполняем один-единственный запрос
    result = await db.execute(query)

    # 3. Достаем уникальные задачи (unique() нужен при joinedload со связями)
    tasks = result.scalars().unique().all()

    # 4. Теперь никакой магии, данные уже в памяти, ошибки не будет!
    return [{"title": t.title, "author": t.author.username if t.author else "No author"} for t in tasks]


