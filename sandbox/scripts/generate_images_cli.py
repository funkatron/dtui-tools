#!/usr/bin/env python3
"""
CLI script for generating images using the Draw Things API.

This script provides a command-line interface for generating images using
the Draw Things package. It supports various options like model selection,
image dimensions, and batch generation.

Example:
    Generate a single image:
        $ python generate_images_cli.py --prompt "A beautiful sunset"

    Test all available models:
        $ python generate_images_cli.py --models-test
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from draw_things import DrawThingsClient, settings

# Default parameters
DEFAULT_PROMPT = "A beautiful woman with long hair and a red corset"
DEFAULT_WIDTH = settings.DEFAULT_WIDTH
DEFAULT_HEIGHT = settings.DEFAULT_HEIGHT
DEFAULT_STEPS = settings.DEFAULT_STEPS
DEFAULT_SEED = settings.DEFAULT_SEED
DEFAULT_MODEL = settings.DEFAULT_MODEL
DEFAULT_LORAS = settings.DEFAULT_LORAS

def generate_images_for_models(
    client: DrawThingsClient,
    prompt: str,
    width: int,
    height: int,
    steps: int,
    seed: int,
    loras: List[str]
) -> List[str]:
    """Generate images using all available models.

    Args:
        client: DrawThingsClient instance
        prompt: Text prompt for image generation
        width: Image width
        height: Image height
        steps: Number of diffusion steps
        seed: Random seed (-1 for random)
        loras: List of LoRA models to apply

    Returns:
        List of paths to generated images
    """
    # Create output directory with timestamp
    output_dir = Path("models-tests") / datetime.now().isoformat()
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    models = client.get_available_models()

    for model in models:
        try:
            paths = client.generate_image(
                prompt=prompt,
                width=width,
                height=height,
                steps=steps,
                seed=seed,
                model=model,
                loras=loras,
                output_dir=str(output_dir)
            )
            saved_paths.extend(paths)
        except Exception as e:
            print(f"Error generating image for model {model}: {e}")

    return saved_paths

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Image generation script")
    parser.add_argument("--models", action="store_true", help="Return a list of models")
    parser.add_argument("--model", type=str, help="Model to use for image generation", default=DEFAULT_MODEL)
    parser.add_argument("--models-test", action="store_true", help="Generate images with each model available")
    parser.add_argument("--prompt", type=str, help="Text prompt for image generation", default=DEFAULT_PROMPT)
    parser.add_argument("--width", type=int, help="Image width", default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, help="Image height", default=DEFAULT_HEIGHT)
    parser.add_argument("--steps", type=int, help="Number of diffusion steps", default=DEFAULT_STEPS)
    parser.add_argument("--seed", type=int, help="Random seed (-1 for random)", default=DEFAULT_SEED)
    parser.add_argument("--output-dir", type=str, help="Output directory for images")

    args = parser.parse_args()
    client = DrawThingsClient()

    if args.models:  # List available models
        models = client.get_available_models()
        if models:
            print("Available models:", models)
        else:
            print("No models available")
        return

    if args.models_test:  # Generate images for each model
        saved_paths = generate_images_for_models(
            client=client,
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            seed=args.seed,
            loras=DEFAULT_LORAS
        )
        print(f"Generated {len(saved_paths)} images")
    else:  # Generate a single image
        saved_paths = client.generate_image(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            seed=args.seed,
            model=args.model,
            loras=DEFAULT_LORAS,
            output_dir=args.output_dir
        )
        print(f"Generated images saved to: {saved_paths}")

if __name__ == "__main__":
    main()
