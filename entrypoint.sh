#!/bin/sh

echo "Waiting for database..."
python -c "
import socket
import time
while True:
    try:
        socket.create_connection(('db', 5432), timeout=1)
        print('Database is reachable')
        break
    except Exception:
        time.sleep(1)
"

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"