"""
Tests for the generate_images_cli.py script.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sandbox.scripts.generate_images_cli import (
    generate_images_for_models,
    main,
    DEFAULT_PROMPT,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_STEPS,
    DEFAULT_SEED,
    DEFAULT_LORAS,
)
from tests.utils import SAMPLE_BASE64_IMAGE

@pytest.fixture
def mock_client():
    """Mock DrawThingsClient for testing."""
    with patch("sandbox.scripts.generate_images_cli.DrawThingsClient") as mock:
        client = mock.return_value
        # Mock get_available_models
        client.get_available_models.return_value = ["standard", "model1", "model2"]
        # Mock generate_image
        client.generate_image.return_value = ["/path/to/generated_image.png"]
        yield client

def test_generate_images_for_models(mock_client, tmp_path):
    """Test generating images for all models."""
    saved_paths = generate_images_for_models(
        client=mock_client,
        prompt=DEFAULT_PROMPT,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        steps=DEFAULT_STEPS,
        seed=DEFAULT_SEED,
        loras=DEFAULT_LORAS,
    )

    # Check that generate_image was called for each model
    assert mock_client.generate_image.call_count == 3
    assert len(saved_paths) == 3

def test_cli_list_models(mock_client, capsys):
    """Test the --models flag."""
    with patch.object(sys, 'argv', ['script.py', '--models']):
        main()
        captured = capsys.readouterr()
        assert "Available models: ['standard', 'model1', 'model2']" in captured.out

def test_cli_generate_single_image(mock_client, capsys):
    """Test generating a single image with custom parameters."""
    test_args = [
        'script.py',
        '--prompt', 'test prompt',
        '--width', '1024',
        '--height', '768',
        '--steps', '50',
        '--seed', '42',
        '--model', 'test_model',
        '--output-dir', '/test/output'
    ]

    with patch.object(sys, 'argv', test_args):
        main()

        # Check that generate_image was called with correct parameters
        mock_client.generate_image.assert_called_once_with(
            prompt='test prompt',
            width=1024,
            height=768,
            steps=50,
            seed=42,
            model='test_model',
            loras=DEFAULT_LORAS,
            output_dir='/test/output'
        )

def test_cli_models_test(mock_client, capsys):
    """Test the --models-test flag."""
    with patch.object(sys, 'argv', ['script.py', '--models-test']):
        main()
        captured = capsys.readouterr()
        assert "Generated 3 images" in captured.out

def test_cli_default_parameters(mock_client):
    """Test that default parameters are used when not specified."""
    with patch.object(sys, 'argv', ['script.py']):
        main()

        mock_client.generate_image.assert_called_once_with(
            prompt=DEFAULT_PROMPT,
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            steps=DEFAULT_STEPS,
            seed=DEFAULT_SEED,
            model=DEFAULT_MODEL,
            loras=DEFAULT_LORAS,
            output_dir=None
        )

def test_cli_error_handling(mock_client, capsys):
    """Test error handling in the CLI."""
    mock_client.generate_image.side_effect = Exception("Test error")

    with patch.object(sys, 'argv', ['script.py']):
        main()
        captured = capsys.readouterr()
        assert "Generated images saved to: []" in captured.out

def test_example_commands(mock_client):
    """Test the example commands from the docstring."""
    # Test example 1: Generate a single image
    with patch.object(sys, 'argv', ['script.py', '--prompt', 'A beautiful sunset']):
        main()
        mock_client.generate_image.assert_called_with(
            prompt='A beautiful sunset',
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            steps=DEFAULT_STEPS,
            seed=DEFAULT_SEED,
            model=DEFAULT_MODEL,
            loras=DEFAULT_LORAS,
            output_dir=None
        )

    # Test example 2: Test all models
    mock_client.reset_mock()
    with patch.object(sys, 'argv', ['script.py', '--models-test']):
        main()
        assert mock_client.get_available_models.called
        assert mock_client.generate_image.call_count == 3