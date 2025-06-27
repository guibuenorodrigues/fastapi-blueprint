import json
import logging
from typing import Literal

from src.core.config import settings


def get_logging_config(log_format: Literal["plaintext", "json"]):
    """
    Returns a dictionary for logging.config.dictConfig based on the desired format.
    """
    common_formatters = {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": ("%(asctime)s - %(name)s - %(log_color)s%(levelname)s%(reset)s - %(message)s"),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": (
                "%(asctime)s %(name)s %(levelname)s %(message)s "
                "%(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d "
                # "%(request_id)s %(user_id)s %(correlation_id)s %(trace_id)s %(span_id)s"
            ),
            "rename_fields": {
                # Timestamp and basic info
                "asctime": "timestamp",
                "name": "logger",
                "levelname": "level",
                "message": "message",
                # Source code context
                "pathname": "file_path",
                "filename": "file_name",
                "lineno": "line_number",
                "funcName": "function_name",
                "module": "module_name",
                # Process/thread info
                "process": "process_id",
                "processName": "process_name",
                "thread": "thread_id",
                "threadName": "thread_name",
            },
            "static_fields": {
                "app_name": settings.APP_NAME,
                "app_version": settings.APP_VERSION,
                "is_debug_enabled": settings.DEBUG,
                "environment": settings.ENVIRONMENT.value,
            },
            "json_ensure_ascii": False,
            "json_serializer": json.dumps,  # Changed from json_encoder to json_serializer
        },
    }

    config = {
        "version": 1,
        "disable_existing_loggers": False,  # Keep False to not disable other loggers by default
        "formatters": common_formatters,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,  # Use global level for console handler
                "formatter": "colored" if log_format == "plaintext" else "json",
                "stream": "ext://sys.stdout",
            },
            # Optional: File handler, can be adapted for plaintext or JSON
            # "file_handler": {
            #     "class": "logging.handlers.RotatingFileHandler",
            #     "level": settings.LOG_LEVEL,
            #     "formatter": "standard" if log_format == "plaintext" else "json",
            #     "filename": "app.log",
            #     "maxBytes": 10 * 1024 * 1024, # 10 MB
            #     "backupCount": 5,
            # },
        },
        "loggers": {
            # Root logger configuration
            "": {  # This is the root logger
                "handlers": ["console"],  # Add other handlers here if needed, e.g., "file_handler"
                "level": settings.LOG_LEVEL,
                "propagate": False,  # Root logger handles everything itself
            },
            # Specific loggers for libraries to quiet them down
            "uvicorn": {
                "handlers": ["console"],  # Let uvicorn logs go to console
                "level": settings.UVICORN_LOG_LEVEL.upper(),
                "propagate": False,  # Stop propagation for uvicorn so it doesn't get double-handled by root
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.UVICORN_LOG_LEVEL.upper(),
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": settings.ERROR_LOG_LEVEL.upper(),
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.pool": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "httpx": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "httpcore": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "asyncio": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            # Your application's custom loggers
            "api.requests": {
                "handlers": ["console"],
                "level": settings.REQUEST_LOG_LEVEL.upper(),
                "propagate": False,
            },
            "api.errors": {
                "handlers": ["console"],
                "level": settings.ERROR_LOG_LEVEL.upper(),
                "propagate": False,
            },
            # If you want module-level loggers to propagate, set propagate=True
            # and ensure they don't have separate handlers specified here
            # For this setup, we're explicitly handling them to ensure consistency
            # if a logger is accidentally initialized too early.
        },
        # Top-level root logger setup (same as "" above, but explicit)
        "root": {
            "handlers": ["console"],  # This re-confirms handlers for the root
            "level": settings.LOG_LEVEL,
        },
    }
    return config


def setup_logging():
    """
    Sets up the application's logging configuration dynamically based on
    the LOG_FORMAT environment variable.
    """

    log_format = settings.LOG_FORMAT.lower()
    if log_format not in ["plaintext", "json"]:
        print(f"Warning: Invalid LOG_FORMAT '{log_format}'. Defaulting to 'plaintext'.")
        log_format = "plaintext"

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    for name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    config = get_logging_config(log_format)
    logging.config.dictConfig(config)

    print(
        f"Logging configured for '{settings.APP_NAME}' in '{settings.ENVIRONMENT.value}' "
        f"environment using '{log_format}' format."
    )


# def setup_logging():
#     """
#     Sets up the application's logging configuration.
#     Configures handlers and a formatter on the root logger,
#     and then sets specific levels for various loggers,
#     relying on propagation for centralized handling.
#     """
#     # 1. Define your custom formatter once
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#     # 2. Get the root logger
#     root_logger = logging.getLogger()

#     # Clear existing handlers from the root logger to prevent duplicates
#     # This is crucial if setup_logging might be called multiple times
#     for handler in root_logger.handlers[:]:
#         root_logger.removeHandler(handler)

#     # Set the overall minimum level for the root logger.
#     # Messages below this level will be discarded by the root logger itself.
#     root_logger.setLevel(settings.LOG_LEVEL.upper())

#     # 3. Add handlers to the root logger only
#     # Console Handler
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(formatter)
#     root_logger.addHandler(console_handler)

#     # Optional: File Handler for all logs
#     # Ensure log directory exists
#     # log_dir = Path("logs")
#     # log_dir.mkdir(parents=True, exist_ok=True)
#     # file_handler_path = log_dir / "app.log"
#     # file_handler = RotatingFileHandler(
#     #     file_handler_path,
#     #     maxBytes=10 * 1024 * 1024, # 10 MB
#     #     backupCount=5
#     # )
#     # file_handler.setFormatter(formatter)
#     # root_logger.addHandler(file_handler)

#     # 4. Configure specific loggers by setting their levels
#     # These loggers will propagate messages up to the root logger's handlers,
#     # but their individual levels control what messages they initially accept.

#     # FastAPI/Uvicorn related loggers
#     logging.getLogger("uvicorn.access").setLevel(os.getenv("REQUEST_LOG_LEVEL", "INFO").upper())
#     logging.getLogger("uvicorn.error").setLevel(os.getenv("ERROR_LOG_LEVEL", "ERROR").upper())
#     # You might want to set uvicorn's root level for its non-access/error logs
#     logging.getLogger("uvicorn").setLevel(settings.LOG_LEVEL.upper())

#     # Database related loggers
#     logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Suppress verbose SQL query logging
#     logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)  # Suppress connection pool logging

#     # HTTP client loggers (e.g., used by FastAPI/Starlette for requests)
#     logging.getLogger("httpx").setLevel(logging.WARNING)
#     logging.getLogger("httpcore").setLevel(logging.WARNING)

#     # Other common library loggers you might want to quiet down
#     logging.getLogger("asyncio").setLevel(logging.WARNING)
#     logging.getLogger("aiosqlite").setLevel(logging.WARNING)
#     logging.getLogger("alembic").setLevel(logging.INFO)  # For database migrations

#     # Your application's custom loggers (these will usually inherit root_logger's level,
#     # but you can explicitly set them if needed for finer control)
#     logging.getLogger("api.requests").setLevel(settings.REQUEST_LOG_LEVEL.upper())
#     logging.getLogger("api.errors").setLevel(settings.ERROR_LOG_LEVEL.upper())

#     logging.info(
#         f"Logging configured. Root logger level: {root_logger.level} ({logging.getLevelName(root_logger.level)})"
#     )
#     # for handler in root_logger.handlers:
#     #     print(f"  Root handler: {type(handler).__name__} with formatter: {handler.formatter._fmt}")


# # To run this example:
# # 1. Save the code above to a file (e.g., main.py).
# # 2. Make sure you have uvicorn installed: pip install uvicorn
# # 3. Run from your terminal: uvicorn main:app --log-config=null --log-level info
# #    The --log-config=null is important to prevent uvicorn from overriding your custom logging config.
# #    You can set --log-level to info or debug to see more details.
