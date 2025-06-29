from datetime import datetime, timedelta, timezone


def utcnow():
    return datetime.now(timezone.utc)


def format_duration(duration: timedelta) -> str:
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"
