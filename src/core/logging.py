import logging
import os
from functools import lru_cache


def setup_logging():
    """
    Sets up the application's logging configuration.
    Configures console, file, and potentially request-specific loggers.
    """
    # Root logger configuration
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output to console
        ],
    )

    # File handler for all logs (optional, for persistent logs)
    # log_file_path = "app.log"
    # file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    # file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    # logging.getLogger().addHandler(file_handler) # Add to root logger

    # Specific logger for API requests (used by middleware)
    request_logger = logging.getLogger("api.requests")
    request_logger.setLevel(os.getenv("REQUEST_LOG_LEVEL", "INFO").upper())
    # You might want a separate handler for request logs to a different file/system

    # Specific logger for API errors (used by middleware)
    error_logger = logging.getLogger("api.errors")
    error_logger.setLevel(os.getenv("ERROR_LOG_LEVEL", "ERROR").upper())

    # Suppress verbose loggers from libraries if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )  # Avoid excessive SQL logging


@lru_cache
def get_logger():
    pass
