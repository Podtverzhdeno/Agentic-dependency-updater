from fastmcp import FastMCP, Context
import os

# Импорт логики инструментов
from mcp_server.tools.scan_project import scan_project
from mcp_server.tools.parse_requirements import parse_requirements
from mcp_server.tools.parse_pyproject import parse_pyproject
from mcp_server.tools.fetch_latest_version import fetch_latest_version
from mcp_server.tools.compare_versions import compare_versions
from mcp_server.tools.update_dependency_file import update_dependency_file
from mcp_server.tools.save_to_history import save_to_history
from mcp_server.tools.generate_report import generate_report
from mcp_server.tools.analyze_breaking_changes import analyze_breaking_changes  # <-- ДОБАВЛЕНО

# Инициализация сервера
mcp = FastMCP(
    "Agentic Dependency Updater",
    instructions="Сервер для автоматического управления жизненным циклом зависимостей Python-проектов."
)

@mcp.tool()
def ping(message: str = "Hello MCP") -> str:
    """Проверка связи с сервером."""
    return f"Pong: {message}"

@mcp.tool()
async def tool_scan_project(path: str, ctx: Context) -> list:
    """Находит файлы зависимостей в проекте."""
    await ctx.info(f"Начинаю сканирование директории: {path}")
    return scan_project(path)

@mcp.tool()
async def tool_parse_dependencies(file_path: str, ctx: Context) -> list:
    """Извлекает пакеты из requirements.txt или pyproject.toml."""
    await ctx.info(f"Парсинг файла: {file_path}")
    if file_path.endswith('.txt'):
        return parse_requirements(file_path)
    return parse_pyproject(file_path)

@mcp.tool()
async def tool_get_latest_and_compare(package: str, current_version: str, ctx: Context) -> dict:
    """Получает версию из PyPI и определяет тип обновления."""
    await ctx.debug(f"Запрос PyPI для пакета: {package}")
    latest_data = fetch_latest_version(package)

    if "error" in latest_data:
        return latest_data

    comparison = compare_versions(current_version, latest_data["latest_version"])
    return {**latest_data, **comparison}

# НОВЫЙ ИНСТРУМЕНТ для анализа рисков с помощью LLM
@mcp.tool()
async def tool_analyze_update_risk(package: str, current_version: str, target_version: str, ctx: Context) -> dict:
    """Анализирует риски обновления пакета с помощью LLM."""
    await ctx.info(f" Анализ рисков для {package}: {current_version} → {target_version}")

    try:
        # Создаем LLM для этого вызова
        from langchain_ollama import ChatOllama
        llm = ChatOllama(
            model="qwen2.5:7b",
            temperature=0,
            base_url="http://localhost:11434"
        )

        result = analyze_breaking_changes(package, current_version, target_version, llm)

        if result.get("is_safe"):
            await ctx.info(f" Безопасное обновление: {result.get('reasoning', '')}")
        else:
            await ctx.warning(f"️ Рискованное обновление: {result.get('reasoning', '')}")

        return result
    except Exception as e:
        await ctx.error(f"Ошибка анализа: {str(e)}")
        return {
            "is_safe": False,
            "risk_level": "High",
            "breaking_changes": ["Ошибка анализа"],
            "reasoning": f"Техническая ошибка: {str(e)}"
        }

@mcp.tool()
async def tool_apply_update(file_path: str, package: str, new_version: str, db_path: str, ctx: Context) -> dict:
    """Физически обновляет файл и сохраняет действие в историю."""
    await ctx.info(f"Обновление {package} до {new_version} в {file_path}")

    update_result = update_dependency_file(file_path, package, new_version)

    if update_result.get("success"):
        history_data = {
            "package": package,
            "old_version": "unknown", # Можно расширить передачу старой версии
            "new_version": new_version,
            "status": "success"
        }
        save_to_history(db_path, history_data)

    return update_result

@mcp.tool()
async def tool_generate_final_report(results: list, project_path: str, ctx: Context) -> str:
    """Создает итоговый Markdown-отчет."""
    await ctx.info("Генерация финального отчета...")
    return generate_report(results, project_path)



if __name__ == "__main__":
    # Запуск в режиме streamable-http
    mcp.run(transport="http", port=8000)