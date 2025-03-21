#!/usr/bin/env python3
import base64
import argparse
from typing import List

import requests

# API endpoint for Draw Things
api_url = "http://localhost:9999/sdapi/v1/txt2img"


# Function to generate an image
def generate_images(prompt, width, height, steps, seed, model, loras):
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "seed": seed,
        "model": model,
        "loras": loras
    }
    response = requests.post(api_url, json=payload)
    if response.status_code != 200:
        print(f"Error getting models: {response.status_code} {response.text} {response.url}")
        return None
    return response.json().get('images', [])


def save_images(images, model_name=None, output_dir=None) -> List[str]:

    written_image_paths = []

    if not images:
        raise Exception

    for i, img_data in enumerate(images):
        img_bytes = base64.b64decode(img_data)
        if model_name and output_dir:
            img_file_path = f"{output_dir}/generated_image_{str(i + 1).zfill(6)}-{model_name}.png"
        else:
            img_file_path = f"generated_image_{i}.png"
        with open(img_file_path, "wb") as img_file:
            img_file.write(img_bytes)
            written_image_paths.append(img_file_path)

    return written_image_paths

def get_models():
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error getting models: {response.status_code} {response.text} {response.url}")
        return None
    return response.json().get('models', [])


def generate_images_for_models(models, **kwargs):
    from datetime import datetime
    import os

    if not models:
        models = get_models()

    output_dir = f"./models-tests/{datetime.now().isoformat()}"
    os.makedirs(output_dir, exist_ok=True)

    images = []

    for model in models:
        images = generate_images(model=model, **kwargs)
        if not images:
            print(f"Error generating image for model {model}: {kwargs}")

    return images


DEFAULT_PROMPT = f"""A beautiful woman with long hair and a red corset"""
DEFAULT_MODEL = "standard"
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 30
DEFAULT_SEED = -1
DEFAULT_LORAS = []


def main():
    parser = argparse.ArgumentParser(description="Image generation script")
    parser.add_argument("--models", action="store_true", help="Return a list of models")
    parser.add_argument("--model", type=str, help="Model to use for image generation", default=DEFAULT_MODEL)
    parser.add_argument("--models-test", action="store_true", help="Generate images with each model available")
    args = parser.parse_args()

    if args.models:  # dump the models
        return output_models()

    if args.models_test:  # generate images for each model
        images = generate_images_for_models(models=get_models(), prompt=DEFAULT_PROMPT, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                                            steps=DEFAULT_STEPS, seed=DEFAULT_SEED, loras=DEFAULT_LORAS)
    else:
        images = generate_images(
            prompt=DEFAULT_PROMPT,
            width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, steps=DEFAULT_STEPS, seed=DEFAULT_SEED,
            model=args.model,
            loras=DEFAULT_LORAS
        )


    save_images(images, model_name=args.model)


def output_models():
    models = get_models()
    if models:
        print("Available models:", models)
    else:
        print("No models available")
    return


if __name__ == "__main__":
    main()
