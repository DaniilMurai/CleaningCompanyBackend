import i18n

import loggers
from config import settings

logger = loggers.JSONLogger("locale_logger")

# В utils/init_i18n.py
_i18n_initialized = False


def init_i18n_once():
    global _i18n_initialized
    if _i18n_initialized:
        return

    i18n.load_path.append(settings.LOCALES_PATH)
    i18n.config.set("file_format", "json")
    i18n.config.set("filename_format", "{locale}.{format}")
    i18n.set("fallback", "ru")
    i18n.set("locale", settings.DEFAULT_LANG)
    _i18n_initialized = True


def init_i18n():
    i18n.load_path.append(settings.LOCALES_PATH)
    i18n.config.set("file_format", "json")
    i18n.config.set("filename_format", "{locale}.{format}")


def keys_locale_map(data: dict, locale: str) -> dict:
    return {i18n.t(k, locale=locale): v for k, v in data.items()}


LOCALIZABLE_FIELDS = {"status"}


def locale_str(data_to_locale: str, locale: str) -> str:
    init_i18n_once()

    v = i18n.t(data_to_locale, locale=locale)
    print("value: ", v)
    return v


def locale_export_reports(data: dict, locale: str) -> dict:
    init_i18n_once()

    localized = {}
    for k, v in data.items():
        translated_key = i18n.t(k, locale=locale)
        if k in LOCALIZABLE_FIELDS:
            translated_value = i18n.t(v, locale=locale)
        else:
            translated_value = v
        localized[translated_key] = translated_value
    return localized
