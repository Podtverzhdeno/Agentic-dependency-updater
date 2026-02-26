import tomllib
import re
from typing import List, Dict, Any

def parse_pyproject(file_path: str) -> List[Dict[str, str]]:
    """
    Парсит pyproject.toml для извлечения зависимостей проекта.
    Поддерживает стандарт PEP 621 и формат Poetry.

    Args:
        file_path (str): Полный путь к файлу pyproject.toml.

    Returns:
        List[Dict[str, str]]: Список зависимостей (пакет и версия).
    """
    dependencies = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = tomllib.load(f)

        # 1. Проверка стандартного формата PEP 621 [project.dependencies]
        # Обычно это список строк типа ["requests>=2.28.0", "flask"]
        project_deps = data.get("project", {}).get("dependencies", [])
        if project_deps:
            for dep in project_deps:
                # Регулярное выражение для отделения имени от версии
                match = re.match(r'^([a-zA-Z0-9\-_]+)(.*)', dep)
                if match:
                    name, version_spec = match.groups()
                    dependencies.append({
                        "name": name,
                        "version": version_spec.strip() if version_spec else "latest"
                    })

        # 2. Проверка формата Poetry [tool.poetry.dependencies]
        # Обычно это словарь типа {"requests": "^2.28.0", "python": "^3.10"}
        poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        if poetry_deps:
            for name, version in poetry_deps.items():
                if name.lower() == "python": # Пропускаем версию самого Python
                    continue
                dependencies.append({
                    "name": name,
                    "version": str(version) if version else "latest"
                })

    except Exception as e:
        # Возврат структурированной ошибки для LLM
        return [{"error": f"Failed to parse toml at {file_path}: {str(e)}"}]

    return dependencies