from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Sendy API. Development"

    logging_level: str = "DEBUG"

    class Config(AppSettings.Config):
        env_file = ".env"
