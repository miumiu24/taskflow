FROM python:3.14-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем всё содержимое
COPY . .

# Устанавливаем проект вместе с зависимостями (включая dev)
RUN pip install --no-cache-dir -e ".[dev]"

# Копируем и настраиваем entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]