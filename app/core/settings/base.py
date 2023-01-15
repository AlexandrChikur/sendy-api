from enum import Enum
from pathlib import Path

from pydantic import BaseSettings

APP_DIR = Path(__file__).parent.parent.parent
ROOT_DIR = APP_DIR.parent


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod

    class Config:
        env_file = ROOT_DIR.joinpath(".env")
