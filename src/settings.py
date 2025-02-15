from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    GROQ_API_KEY: str
    GOOGLE_API_KEY: str
    COMPOSIO_API_KEY: str
    TAVILY_API_KEY: str

    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash"

    EMBEDDING_MODEL: str = "cohere:embed-multilingual-v3.0"
    EMBED_MODEL_DIMENSIONS: int = 1024

    USER_MEMORY_ID: str = "aasherkamal216"
settings = Settings()