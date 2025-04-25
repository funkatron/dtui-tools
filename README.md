# Draw Things API Client

A Python client for interacting with the Draw Things API, providing a simple python interface for image generation and model management.
- Currently, only the HTTP interface is supported.

## Installation

### Using uv (Recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/draw-things.git
cd draw-things

# Install dependencies (uv will automatically create and use a virtual environment)
uv pip install -e .
```

### Using system Python on macOS

```bash
# Clone the repository
git clone https://github.com/yourusername/draw-things.git
cd draw-things

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## Usage

```python
from draw_things.api.client import DrawThingsClient

# Initialize the client
client = DrawThingsClient()

# Get available models
models = client.get_available_models()
print(f"Available models: {models}")

# Generate an image
result = client.generate_image(
    prompt="A beautiful sunset over mountains",
    model="icatcher_realistic_f16.ckpt",  # Optional: specify a model
    width=512,                            # Optional: specify width
    height=512,                           # Optional: specify height
    steps=20,                             # Optional: specify steps
    seed=42,                              # Optional: specify seed
    negative_prompt="blurry, low quality", # Optional: specify negative prompt
    guidance_scale=7.5,                   # Optional: specify guidance scale
    sampler="DPM++ 2M Karras",           # Optional: specify sampler
    clip_skip=1                           # Optional: specify CLIP skip
)

# The image will be saved to the output directory
print(f"Image saved to: {result}")
```

## Configuration

The client can be configured through environment variables or by modifying the settings in `src/draw_things/config/settings.py`:

- `DRAW_THINGS_API_URL`: The URL of the Draw Things API (default: "http://localhost:7860")
- `DRAW_THINGS_DEFAULT_MODEL`: The default model to use for image generation
- `DRAW_THINGS_DEFAULT_WIDTH`: The default width for generated images
- `DRAW_THINGS_DEFAULT_HEIGHT`: The default height for generated images
- `DRAW_THINGS_DEFAULT_STEPS`: The default number of steps for image generation
- `DRAW_THINGS_DEFAULT_SEED`: The default seed for image generation
- `DRAW_THINGS_DEFAULT_GUIDANCE_SCALE`: The default guidance scale for image generation
- `DRAW_THINGS_DEFAULT_SAMPLER`: The default sampler to use
- `DRAW_THINGS_DEFAULT_CLIP_SKIP`: The default CLIP skip value
- `DRAW_THINGS_OUTPUT_DIR`: The directory where generated images will be saved

## Development

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- A running instance of the Draw Things API

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/yourusername/draw-things.git
cd draw-things

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.