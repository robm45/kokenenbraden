import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # ---------- FORMATTERS ----------
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname:<7} {name} — {message}",
            "style": "{",
        },
    },

    # ---------- HANDLERS ----------
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "django_prod.log"),
            "formatter": "verbose",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 5,             # 5 oude logbestanden bewaren
            "encoding": "utf-8",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },

    # ---------- ROOT LOGGER ----------
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },

    # ---------- DJANGO LOGGERS ----------
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

