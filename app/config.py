from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "iris-api"
    app_version: str = "1.0.0"

    log_level: str = "INFO"

    metrics_enabled: bool = True

    mlflow_tracking_uri: str
    model_name: str
    model_version: str


settings = Settings()
