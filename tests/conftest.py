"""
Pytest configuration and fixtures.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from .utils import SAMPLE_BASE64_IMAGE

@pytest.fixture
def mock_api_response():
    """Fixture providing a mock API response."""
    return {
        "images": [SAMPLE_BASE64_IMAGE],
        "models": ["standard", "model1", "model2"]
    }

@pytest.fixture
def mock_urlopen(mock_api_response):
    """Fixture mocking urllib.request.urlopen."""
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_api_response).encode('utf-8')
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response

    with patch('urllib.request.urlopen', return_value=mock_context) as mock:
        yield mock

@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture providing a temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir