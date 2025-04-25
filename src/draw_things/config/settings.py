"""
Configuration settings for the Draw Things API.
"""

from pathlib import Path
from typing import List, Optional

class Settings:
    """Configuration settings."""

    def __init__(self):
        """Initialize settings with default values."""
        # API settings
        self.API_URL = "http://localhost:7860/api/v1/txt2img"

        # Default generation parameters
        self.DEFAULT_MODEL = "icatcher_realistic_f16.ckpt"
        self.DEFAULT_WIDTH = 1088
        self.DEFAULT_HEIGHT = 1920
        self.DEFAULT_STEPS = 32
        self.DEFAULT_SEED = -1
        self.DEFAULT_LORAS: List[str] = []
        self.DEFAULT_NEGATIVE_PROMPT = ""
        self.DEFAULT_GUIDANCE_SCALE = 5.8
        self.DEFAULT_SAMPLER = "DPM++ 2M Karras"
        self.DEFAULT_CLIP_SKIP = 1

        # Output settings
        self.OUTPUT_DIR: Optional[str] = None

settings = Settings()