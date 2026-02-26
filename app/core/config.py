"""
Application configuration loaded from environment variables.

All secrets and environment-specific values are read from .env (or os.environ).
Never hardcode API keys or credentials.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Central config: env vars and paths. Loaded from .env in project root."""

    model_config = SettingsConfigDict(
        env_file=str(_project_root() / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Paths (relative to project root) ---
    project_root: Path = Field(default_factory=_project_root)
    data_dir: Path = Field(default=Path("data"), description="Root for raw and processed data")

    # --- YouTube / Audio ---
    yt_dlp_audio_format: str = Field(default="bestaudio/best", description="yt-dlp audio format")
    yt_dlp_extract_audio: bool = Field(default=True, description="Extract audio only")

    # --- Transcription (Whisper-compatible API or local) ---
    whisper_model: str = Field(default="base", description="Whisper model size")
    transcription_service: str = Field(default="openai", description="openai | local | other")

    # --- Embeddings ---
    embedding_model_name: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        description="Multilingual sentence-transformers model",
    )

    # --- Vector DB (Supabase pgvector) ---
    supabase_url: Optional[str] = Field(default=None, description="Supabase project URL")
    supabase_key: Optional[str] = Field(default=None, description="Supabase anon/service key")
    supabase_jokes_table: str = Field(default="jokes", description="Table name for joke vectors")

    # --- LLM (Groq) ---
    groq_api_key: Optional[str] = Field(default=None, description="Groq API key")
    groq_model: str = Field(default="llama-3.1-70b-versatile", description="Groq model id")

    # --- Joke segmentation / metadata (LLM) ---
    segmentation_model: Optional[str] = Field(default=None, description="Model for segmentation; falls back to groq_model")
    metadata_model: Optional[str] = Field(default=None, description="Model for metadata; falls back to groq_model")

    @property
    def raw_audio_dir(self) -> Path:
        return self.project_root / self.data_dir / "raw_audio"

    @property
    def raw_transcripts_dir(self) -> Path:
        return self.project_root / self.data_dir / "raw_transcripts"

    @property
    def processed_jokes_dir(self) -> Path:
        return self.project_root / self.data_dir / "processed_jokes"

    @property
    def scripts_dir(self) -> Path:
        return self.project_root / self.data_dir / "scripts"

    def ensure_data_dirs(self) -> None:
        """Create data directories if they do not exist."""
        for path in (
            self.raw_audio_dir,
            self.raw_transcripts_dir,
            self.processed_jokes_dir,
            self.scripts_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Return singleton settings instance. Loads .env from project root."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_data_dirs()
    return _settings
