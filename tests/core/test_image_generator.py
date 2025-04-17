"""
Tests for the core image generator.
"""

import pytest
from pathlib import Path
from draw_things.core.image_generator import ImageGenerator, ImageGenerationError
from tests.utils import SAMPLE_BASE64_IMAGE

def test_generate_images(mock_urlopen):
    """Test image generation with mocked API."""
    generator = ImageGenerator()
    images = generator.generate_images(
        prompt="test prompt",
        width=512,
        height=512,
        steps=30,
        seed=42,
        model="standard"
    )

    assert len(images) == 1
    assert images[0] == SAMPLE_BASE64_IMAGE
    mock_urlopen.assert_called_once()

def test_save_images(temp_output_dir):
    """Test saving images to disk."""
    generator = ImageGenerator()
    images = [SAMPLE_BASE64_IMAGE]

    saved_paths = generator.save_images(
        images=images,
        model_name="test_model",
        output_dir=str(temp_output_dir)
    )

    assert len(saved_paths) == 1
    assert Path(saved_paths[0]).exists()
    assert "test_model" in saved_paths[0]

def test_get_available_models(mock_urlopen):
    """Test getting available models."""
    generator = ImageGenerator()
    models = generator.get_available_models()

    assert len(models) == 3
    assert "standard" in models
    assert "model1" in models
    assert "model2" in models
    mock_urlopen.assert_called_once()

def test_generate_images_error():
    """Test error handling in image generation."""
    generator = ImageGenerator()

    with pytest.raises(ImageGenerationError) as exc_info:
        generator.generate_images(prompt="test prompt")

    assert "HTTP Error" in str(exc_info.value) or "URL Error" in str(exc_info.value)

def test_save_images_error():
    """Test error handling in image saving."""
    generator = ImageGenerator()

    with pytest.raises(ImageGenerationError) as exc_info:
        generator.save_images(images=[])

    assert "No images to save" in str(exc_info.value)