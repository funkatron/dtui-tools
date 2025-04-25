"""
Public API interface for Draw Things.
"""

from typing import List, Optional
from ..core.image_generator import ImageGenerator, ImageGenerationError
from ..config.settings import settings

class DrawThingsClient:
    """Public API interface for Draw Things."""

    def __init__(self, api_url: Optional[str] = None):
        """Initialize the client.

        Args:
            api_url: Optional custom API URL
        """
        self._generator = ImageGenerator(api_url or settings.API_URL)

    def generate_image(
        self,
        prompt: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        seed: Optional[int] = None,
        model: Optional[str] = None,
        loras: Optional[List[str]] = None,
        output_dir: Optional[str] = None
    ) -> List[str]:
        """Generate and save an image.

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
            output_dir: Directory to save the image

        Returns:
            List of paths to saved images

        Raises:
            ImageGenerationError: If image generation fails
        """
        # Use settings defaults if parameters not provided
        width = width or settings.DEFAULT_WIDTH
        height = height or settings.DEFAULT_HEIGHT
        steps = steps or settings.DEFAULT_STEPS
        seed = seed or settings.DEFAULT_SEED
        model = model or settings.DEFAULT_MODEL
        loras = loras or settings.DEFAULT_LORAS
        output_dir = output_dir or settings.OUTPUT_DIR

        # Generate images
        images = self._generator.generate_images(
            prompt=prompt,
            width=width,
            height=height,
            steps=steps,
            seed=seed,
            model=model,
            loras=loras,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            sampler=sampler,
            clip_skip=clip_skip
        )

        # Save images
        return self._generator.save_images(
            images=images,
            model_name=model,
            output_dir=output_dir
        )

    def get_available_models(self) -> List[str]:
        """Get list of available models.

        Returns:
            List of available model names

        Raises:
            ImageGenerationError: If model list retrieval fails
        """
        return self._generator.get_available_models()