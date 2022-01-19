import logging
import os
import sys
from typing import Any, Dict, Tuple, Type

from fastapi_cloudauth.cognito import CognitoClaims
from loguru import logger
from pydantic import BaseModel

from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    """
    Base Application settings class.
    """

    debug: bool = False
    api_v1_prefix: str = "/v1"
    title: str = "AWS Serverless FastAPI application"
    version: str = "0.0.1"

    jwt_token_prefix: str = "Bearer"

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # Cognito settings
    aws_region: str = os.getenv("AWS_REGION")
    userpool_id: str = os.getenv("USERPOOL_ID")
    app_client_id: str = os.getenv("APP_CLIENT_ID")

    user_info_class: Type[BaseModel] = CognitoClaims  # use default CognitoClaims schema

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """
        FastAPI related arguments.
        """
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
