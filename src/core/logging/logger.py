import logging
import logging.handlers
import os

import structlog

from core.config.settings import settings


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    log_level = logging.INFO if settings.app_env == "production" else logging.DEBUG

    # Configure structlog
    if settings.app_env == "production":
        processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]

        # File handlers for production
        json_handler = logging.handlers.RotatingFileHandler(
            "logs/application.json.log", maxBytes=10 * 1024 * 1024, backupCount=5
        )
        json_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        logging.basicConfig(
            format="%(message)s", level=log_level, handlers=[json_handler, console_handler]
        )
    else:
        processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ]
        logging.basicConfig(level=log_level)

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def setup_logger(name="reconx"):
    setup_logging()
    return structlog.get_logger(name)
