from typing import Callable

from fastapi import FastAPI

from app.core.auth import init_auth
from app.core.settings.app import AppSettings


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:
    def start_app() -> None:
        init_auth(app, settings)

    return start_app
