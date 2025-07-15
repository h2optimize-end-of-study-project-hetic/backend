import json
import logging
from typing import ClassVar
from datetime import UTC, datetime

from app.src.presentation.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "file": record.pathname,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[104m\033[30m",
        "INFO": "\033[102m\033[30m",
        "WARNING": "\033[103m\033[30m",
        "ERROR": "\033[101m\033[30m",
        "CRITICAL": "\033[41m\033[30m",
    }
    RESET = "\033[0m"

    def format(self, record):
        original_levelname = record.levelname
        space_padding = 10 - len(original_levelname) - 2
        padded_levelname = f" {original_levelname} " + (" " * space_padding)
        color = self.COLORS.get(original_levelname, "")
        record.levelname = f"{color}{padded_levelname}{self.RESET}"

        formatted = super().format(record)

        record.levelname = original_levelname
        return formatted


handlers = ["console"]
log_handlers = {
    "console": {
        "class": "logging.StreamHandler",
        "level": settings.LOG_LEVEL,
        "formatter": "color",
        "stream": "ext://sys.stdout",
    }
}

if settings.LOG_FILE_PATH:
    handlers.append("rotating_file")
    log_handlers["rotating_file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "level": settings.LOG_LEVEL,
        "formatter": "json",
        "filename": settings.LOG_FILE_PATH,
        "maxBytes": 10485760,
        "backupCount": 5,
    }


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%H:%M:%S %z",
        },
        "color": {
            "()": ColorFormatter,
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
            "datefmt": "%H:%M:%S %z",
        },
        "json": {"()": JsonFormatter},
    },
    "handlers": log_handlers,
    "loggers": {
        "app": {"handlers": handlers, "level": settings.LOG_LEVEL, "propagate": False},
        "uvicorn": {
            "handlers": handlers,
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "ERROR",
            "handlers": handlers,
            "propagate": False,
        },
        "fastapi": {
            "handlers": handlers,
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "alembic": {
            "handlers": handlers,
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "starlette": {
            "handlers": handlers,
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {"handlers": handlers, "level": settings.LOG_LEVEL},
}


def setup_logging():
    logging.config.dictConfig(log_config)
