from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    # Production Postgres (asyncpg) connection string for the app database.
    # The default below is a PLACEHOLDER — set your real value in a local .env
    # file (see .env.example / AGENTS.md). Never commit real credentials.
    #
    # Local development alternative (requires `pip install aiosqlite`):
    # DATABASE_URL: str = "sqlite+aiosqlite:///./cram_quest.db"
    DATABASE_URL: str = (
        "postgresql+asyncpg://YOUR-DB-USER:YOUR-DB-PASSWORD@YOUR-DB-HOST:5432/YOUR-DB-NAME?ssl=require"
    )

    # JWT signing keys. The defaults are placeholders and are deliberately
    # insecure — ALWAYS set real values in .env before running in any
    # non-trivial environment. Generate strong ones with:
    #   python -c "import secrets; print(secrets.token_urlsafe(64))"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "YOUR-SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY", "YOUR-REFRESH-SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))

    class Config:
        extra = "allow"
        env_file = ".env"  # Load environment variables


settings = Settings()
