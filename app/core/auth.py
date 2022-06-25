from fastapi import FastAPI
from fastapi_cloudauth.cognito import Cognito
from loguru import logger

from app.core.settings.app import AppSettings


def init_auth(app: FastAPI, settings: AppSettings) -> None:
    """
    Initializes Auth client.
    """
    logger.info("Initializing Auth.")

    app.state.auth = Cognito(
        region=settings.aws_region,
        userPoolId=settings.userpool_id,
        client_id=settings.app_client_id,
    )

    logger.info("Auth initialized.")
