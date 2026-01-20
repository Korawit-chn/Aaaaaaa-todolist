"""Pytest configuration and fixtures for testing."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
