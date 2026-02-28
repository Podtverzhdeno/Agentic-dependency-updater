Agentic Dependency Updater
Описание

Agentic Dependency Updater — инструмент для анализа и обновления зависимостей Python-проекта с использованием агентной архитектуры и локальной LLM.

Проект полностью упакован в Docker и включает внутри контейнера:

fastmcp — MCP-сервер

langgraph + langchain — агентная логика

torch + transformers — локальная LLM

SQLite — хранение истории запусков

Важно о размере Docker-образа

Контейнер содержит полноценную локальную LLM (torch + transformers), поэтому итоговый образ весит несколько гигабайт.

Сборка может занимать ~20 минут

Существует аналогичный репозиторий с использованием API_KEY для LLM — в таком варианте Docker-образ значительно меньше.

Клонирование проекта
git clone https://github.com/Podtverzhdeno/Agentic-dependency-updater
cd Agentic-dependency-updater
Сборка Docker-образа
docker build -t agentic-dependency-updater:latest .

Команда:

читает Dockerfile

устанавливает зависимости из requirements.txt

собирает контейнер с локальной LLM

создаёт образ agentic-dependency-updater:latest

Запуск обновления зависимостей

Основная команда:

docker run agentic-dependency-updater update /app/demo_project /app/data/history.db
Параметры

update — режим обновления зависимостей

/app/demo_project — путь к анализируемому проекту внутри контейнера

/app/data/history.db — SQLite база истории

В процессе выполнения контейнер:

сканирует проект

определяет зависимости

проверяет актуальные версии

формирует отчёт

сохраняет историю выполнения

Smoke-тест

Проверка работоспособности:

docker run agentic-dependency-updater update smoke

Команда выполняет тестовый запуск и проверяет корректность работы агентной логики и MCP-интеграции.

Полный цикл работы
git clone https://github.com/Podtverzhdeno/Agentic-dependency-updater
cd Agentic-dependency-updater

docker build -t agentic-dependency-updater:latest .

docker run agentic-dependency-updater update /app/demo_project /app/data/history.db
Особенности

Используется локальная LLM внутри контейнера

Образ весит много из-за torch и зависимостей HuggingFace

Не требуется установка Python или библиотек на хост-машине

Вся логика запускается полностью из Docker

Назначение проекта

Инструмент предназначен для:

анализа зависимостей Python-проекта

выявления устаревших пакетов

автоматизированной проверки обновлений

генерации отчётов с использованием агентной архитектуры

Проект ориентирован на автономную работу без внешних облачных LLM и API.
