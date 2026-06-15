from celery import Celery

# Указываем, что брокер — это наш сервис 'redis' из docker-compose
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def send_email_task(user_email: str, message: str):
    import time
    time.sleep(5)  # Имитация долгой работы
    print(f"Письмо отправлено на {user_email}: {message}")