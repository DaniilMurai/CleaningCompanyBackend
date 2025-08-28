import base64
import os
import uuid
from typing import Literal

import aiofiles

from config import settings


async def convert_base64_to_server_link(
        base64_links: list[str],
        path: Literal["hints", "reports"]
) -> list[str]:
    file_urls = []

    for base64_link in base64_links:
        # Если уже ссылка, просто добавляем
        if base64_link.startswith("http"):
            file_urls.append(base64_link)
            continue

        # Если нет base64-разделителя
        if "," not in base64_link:
            continue

        # Разделяем base64-заголовок и данные
        header, encoded = base64_link.split(",", 1)
        ext = header.split("/")[1].split(";")[0]
        unique_name = f"{uuid.uuid4()}.{ext}"

        # Путь, зависящий от типа
        if path == "hints":
            dir_path = settings.IMAGES_HINTS_DIR
        else:
            dir_path = settings.IMAGES_REPORTS_DIR

        file_path = os.path.join(dir_path, unique_name)

        # Асинхронно сохраняем файл
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(base64.b64decode(encoded))

        # Генерируем ссылку
        file_urls.append(f"{settings.BASE_URL}/images/{path}/{unique_name}")

    return file_urls
