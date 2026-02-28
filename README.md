Agentic Dependency Updater

Agentic Dependency Updater — это инструмент для анализа и обновления зависимостей Python-проекта с использованием агентной архитектуры и локальной LLM.

Проект упакован в Docker и включает внутри контейнера:

fastmcp — MCP-сервер

langgraph + langchain — агентную логику

torch + transformers — локальную LLM

SQLite — историю запусков

Поскольку контейнер содержит локальную LLM (через torch и transformers), итоговый Docker-образ весит много (несколько гигабайт). Придется ждать ~20 минут (есть аналогичный репозиторий, использующий Api_key для LLM, где образ будет значительно меньше)

Клонирование проекта
git clone https://github.com/Podtverzhdeno/Agentic-dependency-updater
cd Agentic-dependency-updater
Сборка Docker-образа
docker build -t agentic-dependency-updater:latest .

Эта команда:

читает Dockerfile

устанавливает все зависимости из requirements.txt

собирает контейнер с локальной LLM

создаёт образ agentic-dependency-updater:latest

Запуск обновления зависимостей

Основная команда запуска:

docker run agentic-dependency-updater update /app/demo_project /app/data/history.db

Где:

update — режим обновления зависимостей

/app/demo_project — путь к анализируемому проекту внутри контейнера

/app/data/history.db — SQLite база истории

Контейнер:

Сканирует проект

Определяет зависимости

Проверяет актуальные версии

Формирует отчёт

Сохраняет историю выполнения

Smoke-тест

Для проверки работоспособности:

docker run agentic-dependency-updater update smoke

Команда выполняет тестовый запуск и проверяет корректность работы агентов и MCP-логики.

Полный цикл работы

Клонирование репозитория

Сборка образа

Запуск команды обновления

git clone https://github.com/Podtverzhdeno/Agentic-dependency-updater
cd Agentic-dependency-updater

docker build -t agentic-dependency-updater:latest .

docker run agentic-dependency-updater update /app/demo_project /app/data/history.db
Особенности

Используется локальная LLM внутри контейнера.

Образ весит много из-за torch и зависимостей HuggingFace.

Не требуется установка Python или библиотек на хост-машине.

Вся логика запускается из Docker.

Назначение проекта

Инструмент предназначен для:

анализа зависимостей Python-проекта

выявления устаревших пакетов

автоматизированной проверки обновлений

генерации отчётов с использованием агентной архитектуры
