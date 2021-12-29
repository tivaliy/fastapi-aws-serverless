from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    """
    Production Application settings class.
    """

    class Config(AppSettings.Config):
        env_file = "prod.env"
