from database import engine, Base
import models  # Обязательно импортируем наши модели, чтобы Алхимия о них узнала

print("Запуск создания таблиц...")

# Магическая команда, которая смотрит на все чертежи,
# унаследованные от Base, и создает их в базе данных через наш engine
Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы в базе данных taskflow_db!")