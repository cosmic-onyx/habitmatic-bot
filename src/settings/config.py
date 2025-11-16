from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.main_settings_service import PROJECT_ROOT_PATH


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    EXTERNAL_API_URL: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT_PATH / '.env',
        extra='allow'
    )

    @property
    def get_async_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


env_settings = Settings()