from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # Application
    app_name: str = "ml-platform-api"
    app_version: str = "1.0.0"
    log_level: str = "INFO"

    # Metrics
    metrics_enabled: bool = True

    # MLflow
    mlflow_tracking_uri: str
    model_name: str = "default-model"
    model_version: str = "latest"
    model_uri: str = "models:/default-model/latest"


settings = Settings()
