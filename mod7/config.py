from filter import Filter
from file_handler_by_levels import FileHandlerByLevels

config_logging = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
      "filter": {
          "()": Filter
      }
    },
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "()": "logging.handlers.TimedRotatingFileHandler",
            "when": "h",
            "interval": 10,
            "backupCount": 5,
            "level": "INFO",
            "formatter": "base",
            "filters": ["filter"],
            "filename": "utils_logs.log",
        },
        "fileByLevels": {
            "()": FileHandlerByLevels,
            "level": "DEBUG",
            "formatter": "base",
        },
        "server": {
            "()": "logging.handlers.HTTPHandler",
            "host": "127.0.0.1:5000",
            "url": "/logs",
            "method": "POST"
        }
    },
    "loggers": {
        "calculate_logger": {
            "level": "DEBUG",
            "handlers": ["console", "fileByLevels"]
        },
        "utils_logger": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        },
        "server_logger": {
            "level": "DEBUG",
            "handlers": ["server"]
        }
    }
}