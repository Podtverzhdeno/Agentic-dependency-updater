import sqlite3
from datetime import datetime
from typing import Dict, Any, Union

def save_to_history(db_path: str, update_data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
    """
    Сохраняет результат операции обновления в базу данных SQLite.
    Это позволяет агенту отслеживать историю изменений и учиться на прошлых запусках.

    Args:
        db_path (str): Путь к файлу базы данных SQLite.
        update_data (Dict): Данные об обновлении (package, old_version, new_version, status).

    Returns:
        Dict: Статус сохранения {'success': bool, 'error': str (optional)}.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS update_history (
                                                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                     package TEXT NOT NULL,
                                                                     old_version TEXT,
                                                                     new_version TEXT,
                                                                     status TEXT, -- 'success', 'failed', 'skipped'
                                                                     timestamp TEXT NOT NULL
                       )
                       ''')

        cursor.execute('''
                       INSERT INTO update_history (package, old_version, new_version, status, timestamp)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (
                           update_data.get("package"),
                           update_data.get("old_version"),
                           update_data.get("new_version"),
                           update_data.get("status"),
                           datetime.now().isoformat()
                       ))

        conn.commit()
        conn.close()
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}