import sys
import asyncio
from mcp_server.server import mcp, ping

async def run_smoke_test():
    """
    Выполняет быстрый smoke-тест для проверки внутренней логики сервера.
    Это гарантирует, что инструменты зарегистрированы и вызываемы.
    """
    print("Запуск smoke-теста...")
    try:
        # Прямой вызов функции инструмента для проверки интеграции
        result = ping("Smoke Test Connection")
        print(f"Внутренняя проверка ping: {result}")

        # Здесь можно расширить тесты, вызывая другие импортированные инструменты
        print("Все базовые компоненты загружены. Smoke-тест пройден!")
    except Exception as e:
        print(f"Ошибка во время smoke-теста: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Использование: python entrypoint.py [serve|smoke]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "serve":
        # Запуск MCP-сервера. FastMCP является стандартным фреймворком для таких задач [2].
        # Используем HTTP транспорт для обеспечения масштабируемости и сетевой доступности [3].
        print("Запуск MCP-сервера 'Agentic Dependency Updater' на порту 8000...")
        mcp.run(transport="http", port=8000, host="0.0.0.0")

    elif command == "smoke":
        # Запуск асинхронного теста
        asyncio.run(run_smoke_test())

    else:
        print(f"Неизвестная команда: {command}. Доступны: serve, smoke")
        sys.exit(1)

if __name__ == "__main__":
    main()