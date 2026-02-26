FROM python:3.11-slim

# Установка системных зависимостей, необходимых для сборки некоторых библиотек
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# ОПТИМИЗАЦИЯ СКОРОСТИ: Устанавливаем 'uv' для быстрой загрузки тяжелых пакетов (torch, transformers)
RUN pip install --no-cache-dir uv

# Копируем только файл зависимостей, чтобы Docker мог закешировать этот слой
# Если список библиотек не меняется, этот этап будет пропускаться при пересборке
COPY requirements.txt .

# Установка зависимостей через uv (работает в разы быстрее стандартного pip)
# Флаг --system позволяет устанавливать пакеты напрямую в систему контейнера
RUN uv pip install --system --no-cache -r requirements.txt

# Копируем весь остальной исходный код проекта
COPY . .

# Подготавливаем директории для эпизодической памяти (SQLite) и тестового проекта
RUN mkdir -p /app/data /app/demo_project

# Открываем порт 8000 для работы MCP-сервера по HTTP
EXPOSE 8000

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/app/data/history.db

# Точка входа в приложение через диспетчер команд
# По умолчанию запускает сервер, но позволяет передать команду 'smoke' для тестов
ENTRYPOINT ["python", "entrypoint.py"]
CMD ["serve"]