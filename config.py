import os
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, conint

BASE_DIR = Path(__file__).resolve().parent
DOTENV_FILE = os.path.join(BASE_DIR, '.env')


class Settings(BaseSettings):
    DELAY: float
    PAGE_LOAD_WAITING_DELAY: float
    SERVICE_ACCOUNT: str
    SHEET_NAME: str


settings = Settings(_env_file=DOTENV_FILE)
