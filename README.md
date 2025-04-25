# Draw Things

A Python package for generating and manipulating images.

## Installation

### Using uv (Recommended)
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv pip install draw-things
```

### Using pip
```bash
pip install draw-things
```

## Usage

```python
from draw_things import DrawThingsClient

# Initialize the client
client = DrawThingsClient()

# Generate an image
image_paths = client.generate_image(
    prompt="A beautiful sunset over mountains",
    model="standard"
)
```

## Development

### Using uv (Recommended)
1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -e .
   ```

### Using venv
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e .
   ```

## Documentation

See the [docs](docs/) directory for detailed documentation.

## License

MIT License