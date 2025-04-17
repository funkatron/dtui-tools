#!/usr/bin/env python3
"""
Basic usage example for Draw Things.
"""

from draw_things import DrawThingsClient

def main():
    # Initialize the client
    client = DrawThingsClient()

    # Get available models
    models = client.get_available_models()
    print(f"Available models: {models}")

    # Generate an image
    prompt = "A beautiful sunset over mountains"
    saved_paths = client.generate_image(
        prompt=prompt,
        model="standard"  # or use any model from the list above
    )

    print(f"Generated images saved to: {saved_paths}")

if __name__ == "__main__":
    main()