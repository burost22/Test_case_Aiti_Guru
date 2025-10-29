from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BD_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str = "db"

    @property
    def database_url(self) -> str:
        """Формирует строку подключения к базе данных."""
        return (
            f"postgresql+asyncpg://"
            f"{self.BD_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
