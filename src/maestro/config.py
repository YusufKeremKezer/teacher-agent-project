from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # --- Brave Search Configuration ---
    BRAVE_SEARCH_API_KEY: str = ""  # Optional - only needed for web search tools
    
    
    # Default models served by the local Ollama instance
    # Switch from Llama 3 to Google's Gemma family per request
    OLLAMA_MODEL_NAME: str = "llama3.1"
    OLLAMA_SUMMARY_MODEL: str = "llama3"
    
    # --- MongoDB Configuration ---
    MONGO_URI: str = Field(
        default="mongodb://maestro:maestro@local_dev_atlas:27017/?directConnection=true",
        description="Connection URI for the local MongoDB Atlas instance.",
    )




    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TEXT_EMBEDDING_MODEL_DIM: int = 384
    RAG_TOP_K: int = 3
    RAG_DEVICE: str = "cpu"
    RAG_CHUNK_SIZE: int = 256


settings = Settings()
