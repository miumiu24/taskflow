import pytest
from models import User


@pytest.mark.asyncio
async def test_create_task(ac, db_session):
    """1. Тест на успешное создание задачи"""

    test_user = User(username="elena")

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    response = await ac.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Desc",
            "user_id": test_user.id
        }
    )

    assert response.status_code == 201

@pytest.mark.asyncio  # <-- Обязательно добавляем для асинхронных тестов
async def test_get_tasks(ac):
    """2. Тест на получение списка задач"""
    response = await ac.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio  # <-- И сюда тоже
async def test_get_task_not_found(ac):
    """3. Тест на ошибку 404"""
    response = await ac.get("/tasks/999999")
    assert response.status_code == 404
