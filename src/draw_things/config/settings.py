"""
Configuration settings for the Draw Things package.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_URL: str = Field(
        default="http://localhost:9999/sdapi/v1/txt2img",
        description="URL of the Draw Things API endpoint"
    )

    # Default Generation Parameters
    DEFAULT_MODEL: str = Field(
        default="standard",
        description="Default model to use for image generation"
    )
    DEFAULT_WIDTH: int = Field(
        default=512,
        description="Default width of generated images"
    )
    DEFAULT_HEIGHT: int = Field(
        default=512,
        description="Default height of generated images"
    )
    DEFAULT_STEPS: int = Field(
        default=30,
        description="Default number of diffusion steps"
    )
    DEFAULT_SEED: int = Field(
        default=-1,
        description="Default random seed (-1 for random)"
    )
    DEFAULT_LORAS: List[str] = Field(
        default_factory=list,
        description="Default LoRA models to apply"
    )

    # Output Configuration
    OUTPUT_DIR: Optional[str] = Field(
        default=None,
        description="Default directory to save generated images"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create a global settings instance
settings = Settings()