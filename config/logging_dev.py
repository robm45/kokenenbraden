import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # ---------- FORMATTERS -----------
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname:<7} {name} — {message}",
            "style": "{",
        },
    },

    # ---------- HANDLERS -------------
    "handlers": {
        # Algemene file logging voor ALLE loggers
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "django_dev.log"),
            "formatter": "verbose",
        },

        # Alleen voor email-debugs, niet normaal gebruik
        "mail_debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "mail_debug.log"),
            "formatter": "verbose",
        },

        # Mail naar ADMINS bij echte errors
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },

    # ---------- ROOT LOGGER ----------
    # ALLES (ook jouw views, libs, applicaties) gaat hierheen
    "root": {
        "handlers": ["file"],
        "level": "DEBUG",
    },

    # ---------- DJANGO LOGGERS -------
    "loggers": {
        # Algemene Django logging
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },

        # Request errors → file + mail
        "django.request": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },

        # Security errors → file + mail
        "django.security": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },

        # E-mail backend debug info (fontTools e.d.)
        "django.core.mail": {
            "handlers": ["mail_debug_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

