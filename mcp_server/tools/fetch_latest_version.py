import re
import asyncio
from typing import Dict, Union
import aiohttp

async def fetch_latest_version(package_name: str) -> Dict[str, Union[str, bool]]:
    """
    Асинхронно запрашивает последнюю версию пакета из PyPI с retry и безопасной обработкой extras.

    Args:
        package_name (str): Имя Python-пакета (например, 'requests' или 'requests[security]').

    Returns:
        Dict: С ключом 'latest_version' или 'error'.
    """
    base_package = re.split(r"[\[\]]", package_name)[0]
    url = f"https://pypi.org/pypi/{base_package}/json"
    max_attempts = 3
    delay = 1

    async with aiohttp.ClientSession() as session:
        for attempt in range(1, max_attempts + 1):
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        latest_version = data.get("info", {}).get("version", "unknown")
                        return {"package": package_name, "latest_version": latest_version}
                    else:
                        error_msg = f"PyPI returned status {resp.status}"
            except Exception as e:
                error_msg = str(e)

            if attempt < max_attempts:
                await asyncio.sleep(delay)
            else:
                return {"package": package_name, "error": error_msg}

    return {"package": package_name, "error": "Unknown error"}