"""
Tests for the API client.
"""

import pytest
from draw_things.api.client import DrawThingsClient
from draw_things.core.image_generator import ImageGenerationError

def test_client_initialization():
    """Test client initialization."""
    client = DrawThingsClient()
    assert client._generator is not None

def test_generate_image(mock_urlopen, temp_output_dir):
    """Test image generation through the client."""
    client = DrawThingsClient()

    saved_paths = client.generate_image(
        prompt="test prompt",
        model="standard",
        output_dir=str(temp_output_dir)
    )

    assert len(saved_paths) == 1
    assert "standard" in saved_paths[0]

def test_get_available_models(mock_urlopen):
    """Test getting available models through the client."""
    client = DrawThingsClient()
    models = client.get_available_models()

    assert len(models) == 3
    assert "standard" in models

def test_generate_image_error():
    """Test error handling in client image generation."""
    client = DrawThingsClient()

    with pytest.raises(ImageGenerationError):
        client.generate_image(prompt="test prompt")

def test_custom_api_url():
    """Test client with custom API URL."""
    custom_url = "http://custom-url/api"
    client = DrawThingsClient(api_url=custom_url)

    assert client._generator.api_url == custom_url