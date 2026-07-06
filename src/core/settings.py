from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    """
    Central application configuration.

    All configuration values are loaded from
    the .env file using Pydantic BaseSettings.
    """

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    app_name: str = "Dirt2Dollar"

    app_version: str = "1.0.0"

    # -------------------------------------------------
    # Supabase
    # -------------------------------------------------

    supabase_url: str = ""

    supabase_key: str = ""

    # -------------------------------------------------
    # Groq
    # -------------------------------------------------

    groq_api_key: str = ""

    groq_model: str = (
        "llama-3.3-70b-versatile"
    )

    # -------------------------------------------------
    # HuggingFace
    # -------------------------------------------------

    huggingface_api_key: str = ""

    embedding_model: str = (
        "BAAI/bge-base-en-v1.5"
    )

    # -------------------------------------------------
    # Google Sheets
    # -------------------------------------------------

    google_sheet_id: str = ""

    google_sheet_name: str = ""

    google_credentials_file: str = (
        "credentials/google_service_account.json"
    )

    # -------------------------------------------------
    # Environment Configuration
    # -------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


# Singleton settings object used
# throughout the application.
settings = Settings()