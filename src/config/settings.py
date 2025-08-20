"""Configuration settings for Markdown Exporter."""

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class ServerConfig(BaseModel):
    """Server configuration settings."""
    
    mcp_port: int = Field(default=8001, description="MCP server port")
    api_port: int = Field(default=8001, description="API server port")
    ollama_host: str = Field(
        default="http://localhost:11434", 
        description="Ollama server host"
    )
    ollama_model: str = Field(
        default="llama3", 
        description="Ollama model to use"
    )


class ConversionConfig(BaseModel):
    """Conversion configuration settings."""
    
    default_format: str = Field(
        default="word", 
        description="Default output format"
    )
    enable_mermaid: bool = Field(
        default=True, 
        description="Enable Mermaid diagram processing"
    )
    enable_images: bool = Field(
        default=True, 
        description="Enable image embedding"
    )
    table_alignment: str = Field(
        default="left", 
        description="Table text alignment"
    )
    remove_unicode: bool = Field(
        default=True, 
        description="Remove unicode characters"
    )
    remove_emoji: bool = Field(
        default=True, 
        description="Remove emoji characters"
    )

    @field_validator("default_format")
    @classmethod
    def validate_default_format(cls, v):
        """Validate default format."""
        if v not in ["word", "pdf", "html"]:
            raise ValueError("default_format must be one of: word, pdf, html")
        return v

    @field_validator("table_alignment")
    @classmethod
    def validate_table_alignment(cls, v):
        """Validate table alignment."""
        if v not in ["left", "center", "right"]:
            raise ValueError("table_alignment must be one of: left, center, right")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(default="json", description="Log format")
    output: str = Field(default="stdout", description="Log output")

    @field_validator("level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"level must be one of: {valid_levels}")
        return v.upper()

    @field_validator("format")
    @classmethod
    def validate_log_format(cls, v):
        """Validate log format."""
        if v not in ["json", "text"]:
            raise ValueError("format must be one of: json, text")
        return v


class SecurityConfig(BaseModel):
    """Security configuration settings."""
    
    allowed_extensions: List[str] = Field(
        default=[".md", ".markdown"], 
        description="Allowed file extensions"
    )
    max_file_size: str = Field(
        default="10MB", 
        description="Maximum file size"
    )
    validate_file_types: bool = Field(
        default=True, 
        description="Validate file types"
    )

    @field_validator("max_file_size")
    @classmethod
    def validate_max_file_size(cls, v):
        """Validate max file size format."""
        if not v.endswith(("B", "KB", "MB", "GB")):
            raise ValueError("max_file_size must end with B, KB, MB, or GB")
        return v


class Settings(BaseSettings):
    """Main application settings."""
    
    server: ServerConfig = Field(default_factory=ServerConfig)
    conversion: ConversionConfig = Field(default_factory=ConversionConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # File paths
    config_file: Optional[Path] = Field(
        default=None, 
        description="Configuration file path"
    )
    output_dir: Path = Field(
        default=Path("results"), 
        description="Output directory"
    )
    temp_dir: Path = Field(
        default=Path("temp"), 
        description="Temporary directory"
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    def __init__(self, **kwargs):
        """Initialize settings with config file support."""
        config_file = kwargs.get("config_file")
        if config_file and Path(config_file).exists():
            # Load from config file
            import yaml
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
                kwargs.update(config_data)
        
        super().__init__(**kwargs)
        
        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def set_settings(settings: Settings) -> None:
    """Set global settings instance."""
    global _settings
    _settings = settings
