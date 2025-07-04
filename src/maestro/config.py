from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # --- Brave Search Configuration ---
    BRAVE_SEARCH_API_KEY: str = ""  # Optional - only needed for web search tools
    GOOGLE_API_KEY: str = ""  # Optional - required only when using Google GenAI models
    
    # Default models served by the local Ollama instance
    # Switch from Llama 3 to Google's Gemma family per request
    GOOGLE_MODEL: str = "gemini-2.5-flash"
    GOOGLE_SUMMARY_MODEL: str = "gemini-1.5-flash"
    
    # --- MongoDB Configuration ---
    MONGO_URI: str = Field(
        default="mongodb+srv://krmkzr:0553298Aa.@cluster0.jn2o4xo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        description="Connection URI for the local MongoDB Atlas instance.",
    )

    MONGO_DB_NAME: str = "maestro"
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "maestro_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "maestro_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION: str = "maestro_long_term_memory"


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


