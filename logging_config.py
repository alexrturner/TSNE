import logging.config

from pythonjsonlogger import jsonlogger

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        "file": {  # New File Handler
            "class": "logging.FileHandler",
            "filename": "app.log",  # Log file path
            "mode": "a",  # Append mode
            "formatter": "json",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["stdout", "file"],  # Added file handler
            "level": "DEBUG",
            "propagate": True,
        }
    },
}

logging.config.dictConfig(LOGGING)