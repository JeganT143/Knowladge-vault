from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Knowledge Vault"
    debug: bool = False

    database_url: str
    database_url_sync: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
