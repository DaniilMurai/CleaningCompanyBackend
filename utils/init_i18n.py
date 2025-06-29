import i18n

from config import settings


def init_i18n():
    i18n.load_path.append(settings.LOCALES_PATH)
    i18n.config.set("file_format", "json")
    i18n.config.set("filename_format", "{locale}.{format}")
