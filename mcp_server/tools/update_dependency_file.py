import re
import tomllib
from typing import Dict

def update_dependency_file(file_path: str, package: str, new_version: str) -> Dict[str, bool]:
    """
    Обновляет версию указанного пакета в файле зависимостей.
    Поддерживает форматы requirements.txt и pyproject.toml.

    Args:
        file_path (str): Путь к файлу для обновления.
        package (str): Имя пакета.
        new_version (str): Новая версия (например, '2.31.0').

    Returns:
        Dict: Статус операции {'success': bool, 'error': str (optional)}.
    """
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            updated = False
            with open(file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if re.match(rf'^{package}(?:==|>=|<=|~=|>|<|$)', line.strip()):
                        f.write(f"{package}=={new_version}\n")
                        updated = True
                    else:
                        f.write(line)
            return {"success": updated}

        elif file_path.endswith('.toml'):
            data = tomllib.load(file_path)
            updated = False

            if "project" in data and "dependencies" in data["project"]:
                deps = data["project"]["dependencies"]
                for i, dep in enumerate(deps):
                    if dep.startswith(package):
                        deps[i] = f"{package}=={new_version}"
                        updated = True

            if "tool" in data and "poetry" in data["tool"] and "dependencies" in data["tool"]["poetry"]:
                poetry_deps = data["tool"]["poetry"]["dependencies"]
                if package in poetry_deps:
                    poetry_deps[package] = new_version
                    updated = True

            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    tomllib.dump(data, f)
            return {"success": updated}

        return {"success": False, "error": "Unsupported file format"}

    except Exception as e:
        return {"success": False, "error": str(e)}