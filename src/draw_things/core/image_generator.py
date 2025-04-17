"""
Core image generation functionality.
"""

import base64
import json
from typing import List, Optional, Dict, Any
import urllib.request
import urllib.error
from pathlib import Path

class ImageGenerationError(Exception):
    """Base exception for image generation errors."""
    pass

class ImageGenerator:
    """Core image generation functionality."""

    def __init__(self, api_url: str = "http://localhost:9999/sdapi/v1/txt2img"):
        """Initialize the image generator.

        Args:
            api_url: URL of the Draw Things API endpoint
        """
        self.api_url = api_url

    def generate_images(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        steps: int = 30,
        seed: int = -1,
        model: str = "standard",
        loras: List[str] = None
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

        Returns:
            List of base64-encoded images

        Raises:
            ImageGenerationError: If image generation fails
        """
        if loras is None:
            loras = []

        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "seed": seed,
            "model": model,
            "loras": loras
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('images', [])
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

        Raises:
            ImageGenerationError: If no images are provided or saving fails
        """
        if not images:
            raise ImageGenerationError("No images to save")

        written_paths = []
        output_path = Path(output_dir) if output_dir else Path.cwd()

        for i, img_data in enumerate(images):
            try:
                img_bytes = base64.b64decode(img_data)
                if model_name:
                    img_file_path = output_path / f"generated_image_{str(i + 1).zfill(6)}-{model_name}.png"
                else:
                    img_file_path = output_path / f"generated_image_{i}.png"

                with open(img_file_path, "wb") as img_file:
                    img_file.write(img_bytes)
                    written_paths.append(str(img_file_path))
            except (base64.binascii.Error, OSError) as e:
                raise ImageGenerationError(f"Error saving image: {str(e)}")

        return written_paths

    def get_available_models(self) -> List[str]:
        """Get list of available models from the API.

        Returns:
            List of available model names

        Raises:
            ImageGenerationError: If model list retrieval fails
        """
        try:
            with urllib.request.urlopen(self.api_url) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('models', [])
        except urllib.error.HTTPError as e:
            raise ImageGenerationError(f"HTTP Error: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            raise ImageGenerationError(f"URL Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise ImageGenerationError(f"JSON Decode Error: {str(e)}")