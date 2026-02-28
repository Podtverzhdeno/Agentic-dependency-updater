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

        project_deps = data.get("project", {}).get("dependencies", [])
        if project_deps:
            for dep in project_deps:
                match = re.match(r'^([a-zA-Z0-9\-_]+)(.*)', dep)
                if match:
                    name, version_spec = match.groups()
                    dependencies.append({
                        "name": name,
                        "version": version_spec.strip() if version_spec else "latest"
                    })

        poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        if poetry_deps:
            for name, version in poetry_deps.items():
                if name.lower() == "python":
                    continue
                dependencies.append({
                    "name": name,
                    "version": str(version) if version else "latest"
                })

    except Exception as e:
        return [{"error": f"Failed to parse toml at {file_path}: {str(e)}"}]

    return dependencies