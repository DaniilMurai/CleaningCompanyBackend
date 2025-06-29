import i18n

from config import settings


def init_i18n():
    i18n.load_path.append(settings.LOCALES_PATH)
    i18n.config.set("file_format", "json")
    i18n.config.set("filename_format", "{locale}.{format}")


def keys_locale_map(data: dict, locale: str) -> dict:
    return {i18n.t(k, locale=locale): v for k, v in data.items()}


LOCALIZABLE_FIELDS = {"status"}


def locale_export_reports(data: dict, locale: str) -> dict:
    return {
        i18n.t(k, locale=locale): (
            i18n.t(v, locale=locale)
            if k in LOCALIZABLE_FIELDS
            else v
        )
        for k, v in data.items()
    }
