"""
Core image generation functionality.
"""

import base64
import json
from typing import List, Optional, Dict, Any
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

from ..config.settings import settings

class ImageGenerationError(Exception):
    """Base exception for image generation errors."""
    pass

class ImageGenerator:
    """Core image generation functionality."""

    def __init__(self, api_url: str = None):
        """Initialize the image generator.

        Args:
            api_url: URL of the Draw Things API endpoint
        """
        self.api_url = api_url or settings.API_URL

    def generate_images(
        self,
        prompt: str,
        width: int = None,
        height: int = None,
        steps: int = None,
        seed: int = None,
        model: str = None,
        loras: List[str] = None,
        negative_prompt: str = None,
        guidance_scale: float = None,
        sampler: str = None,
        clip_skip: int = None
    ) -> List[str]:
        """Generate images using the Draw Things API.

        Args:
            prompt: Text prompt for image generation
            width: Width of the generated image
            height: Height of the generated image
            steps: Number of diffusion steps
            seed: Random seed (-1 for random)
            model: Model to use for generation
            loras: List of LoRA models to apply
            negative_prompt: Negative prompt for image generation
            guidance_scale: Guidance scale for the diffusion process
            sampler: Sampler to use for generation
            clip_skip: Number of CLIP layers to skip

        Returns:
            List of base64-encoded images

        Raises:
            ImageGenerationError: If image generation fails
        """
        if loras is None:
            loras = []

        # Basic payload with required parameters
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt or settings.DEFAULT_NEGATIVE_PROMPT,
            "width": width or settings.DEFAULT_WIDTH,
            "height": height or settings.DEFAULT_HEIGHT,
            "steps": steps or settings.DEFAULT_STEPS,
            "cfg_scale": guidance_scale or settings.DEFAULT_GUIDANCE_SCALE,
            "sampler_name": sampler or settings.DEFAULT_SAMPLER,
            "seed": seed or settings.DEFAULT_SEED,
            "clip_skip": clip_skip or settings.DEFAULT_CLIP_SKIP,
            "batch_size": 1,
            "n_iter": 1,
            "restore_faces": False,
            "enable_hr": False,
            "denoising_strength": 0.7
        }

        # Add LoRA models if specified
        if loras:
            payload["alwayson_scripts"] = {
                "lora": {
                    "args": [{"model": lora} for lora in loras]
                }
            }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                # The API returns the generated image in the response
                if 'images' in result:
                    return result['images']
                else:
                    raise ImageGenerationError("No images in API response")
        except urllib.error.HTTPError as e:
            raise ImageGenerationError(f"HTTP Error: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            raise ImageGenerationError(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise ImageGenerationError(f"JSON Decode Error: {str(e)}")

    def save_images(
        self,
        images: List[str],
        model_name: Optional[str] = None,
        output_dir: Optional[str] = None
    ) -> List[str]:
        """Save base64-encoded images to disk.

        Args:
            images: List of base64-encoded images
            model_name: Name of the model used for generation
            output_dir: Directory to save images to

        Returns:
            List of paths to saved images
        """
        if not images:
            return []

        output_dir = Path(output_dir or settings.OUTPUT_DIR or "generated_images")
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for i, image_data in enumerate(images):
            # Decode base64 image
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                raise ImageGenerationError(f"Error decoding image: {str(e)}")

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}_{i}.png"
            if model_name:
                filename = f"{model_name}_{filename}"

            # Save image
            file_path = output_dir / filename
            try:
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                saved_paths.append(str(file_path))
            except Exception as e:
                raise ImageGenerationError(f"Error saving image: {str(e)}")

        return saved_paths

    def get_available_models(self) -> List[str]:
        """Get list of available models.

        Returns:
            List of available model names

        Raises:
            ImageGenerationError: If model list retrieval fails
        """
        models_url = self.api_url.replace("/txt2img", "/sd-models")
        try:
            with urllib.request.urlopen(models_url) as response:
                result = json.loads(response.read().decode('utf-8'))
                # The API returns a list of model objects
                return [model.get('title', '') for model in result]
        except urllib.error.HTTPError as e:
            raise ImageGenerationError(f"HTTP Error: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            raise ImageGenerationError(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise ImageGenerationError(f"JSON Decode Error: {str(e)}")