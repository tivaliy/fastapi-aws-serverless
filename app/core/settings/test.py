import logging

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    """
    Test Application settings class.
    """

    debug: bool = True

    logging_level: int = logging.DEBUG
