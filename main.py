from fastapi import FastAPI
from app.routers.tasks import router as tasks_router
from celery_app import send_email_task

app = FastAPI(title="TaskFlow API")

# Подключаем наш роутер задач к главному приложению
app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "Главный конвейер работает. Иди в /docs, чтобы увидеть ручки задач!"}

@app.post("/send-email/{email}")
def trigger_email(email: str):
    # .delay() отправляет задачу в Redis, а воркер её подхватывает
    send_email_task.delay(email, "Привет из Docker!")
    return {"message": "Задача на отправку письма принята в очередь"}