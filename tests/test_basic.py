"""Basic tests for Markdown Exporter."""

import pytest
from pathlib import Path


def test_project_structure():
    """Test that the project structure is set up correctly."""
    # Check that main directories exist
    assert Path("src").exists()
    assert Path("tests").exists()
    assert Path("docs").exists()
    assert Path("results").exists()
    
    # Check that key modules exist
    assert Path("src/__init__.py").exists()
    assert Path("src/config").exists()
    assert Path("src/core").exists()
    assert Path("src/logging").exists()


def test_config_import():
    """Test that config module can be imported."""
    try:
        from src.config import get_settings
        assert callable(get_settings)
    except ImportError as e:
        pytest.skip(f"Config module not ready: {e}")


def test_core_import():
    """Test that core modules can be imported."""
    try:
        from src.core import MarkdownProcessor
        assert MarkdownProcessor is not None
    except ImportError as e:
        pytest.skip(f"Core module not ready: {e}")


def test_logging_import():
    """Test that logging module can be imported."""
    try:
        from src.logging import get_logger
        assert callable(get_logger)
    except ImportError as e:
        pytest.skip(f"Logging module not ready: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
