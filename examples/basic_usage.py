#!/usr/bin/env python3
"""
Basic usage example for the Draw Things API.

This example demonstrates how to:
1. Initialize the client
2. Get available models
3. Generate images with different parameters
4. Handle errors
5. Configure output directory

Prerequisites:
- Draw Things API running at http://localhost:7860
"""

import os
from pathlib import Path
from draw_things.api.client import DrawThingsClient
from draw_things.core.image_generator import ImageGenerationError

def main():
    """Demonstrate basic usage of the Draw Things API client."""
    # Initialize the client
    client = DrawThingsClient()

    try:
        # Get available models
        models = client.get_available_models()
        print("Available models:", models)

        # Generate an image with default parameters
        prompt = "A beautiful sunset over a mountain landscape, digital art"
        images = client.generate_image(
            prompt=prompt,
            width=1088,
            height=1920,
            steps=32,
            guidance_scale=5.8,
            sampler="DPM++ 2M Karras",
            clip_skip=1,
            negative_prompt=""
        )

        # Save the generated images
        saved_paths = client.save_images(images)
        print("Images saved to:", saved_paths)

    except ImageGenerationError as e:
        print("Error:", str(e))
    except Exception as e:
        print("Unexpected error:", str(e))

if __name__ == "__main__":
    main()