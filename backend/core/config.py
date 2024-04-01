import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CERTS_PATH = Path(BASE_DIR) / "core" / "auth" / "certs"

load_dotenv(dotenv_path=BASE_DIR / '.env')

class AuthJWT(BaseModel):
    private_key_path: Path = CERTS_PATH / "jwt-private.pem"
    public_key_path: Path = CERTS_PATH / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    # ============  DB SETTINGS ===========
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    DB_ECHO: bool = True
    DB_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # =========== Auth ============
    auth: AuthJWT = AuthJWT()


settings = Settings()
