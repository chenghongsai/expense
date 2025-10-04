from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Docker postgres defaults (can be overridden by env)
    pguser: str = "contoso"
    pgpassword: str = "contoso123"
    pgdatabase: str = "contoso_expense"
    pghost: str = "localhost"
    pgport: int = 5432
    database_url: str | None = None

    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    default_admin_email: str = "admin@contoso.com"
    default_admin_password: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.pguser}:{self.pgpassword}"
            f"@{self.pghost}:{self.pgport}/{self.pgdatabase}"
        )

settings = Settings()
