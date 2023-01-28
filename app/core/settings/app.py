import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import PostgresDsn, SecretStr

from app.core.logging import InterceptHandler
from app.core.logging import rotator
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False

    version: str = "1.2.3"
    api_prefix: str = "/api"

    docs_url: str = "/api/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/api/openapi.json"
    redoc_url: str = "/api/redoc"

    title: str = "Sendy API"
    description: str = (
        "Messages gateway made easy. Here is an HTTP API for work with service."
    )

    database_url: PostgresDsn
    max_connection_count: int = 50
    min_connection_count: int = 50

    secret_key: SecretStr

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: str = "INFO"
    logging_dir_path: Path = "./"

    @property
    def path_to_logfile(self) -> Path:
        return self.logging_dir_path.joinpath("{time:YYYY-MM-DD}_sendy.log")

    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "description": self.description,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(
            handlers=[
                {
                    "sink": sys.stderr,
                    "level": self.logging_level,
                    "diagnose": False,
                    "backtrace": True,
                },
                {
                    "sink": self.path_to_logfile,
                    "level": self.logging_level,
                    "rotation": rotator.should_rotate,
                    "retention": "10 days",
                    "compression": "zip",
                    "backtrace": True,
                    "diagnose": True,
                },
            ]
        )
