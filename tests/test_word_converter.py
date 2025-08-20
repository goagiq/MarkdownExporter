"""Test Word converter functionality."""

import pytest
from pathlib import Path

from src.core.processor import MarkdownProcessor
from src.core.converters import WordConverter


def test_word_converter_basic():
    """Test basic Word conversion functionality."""
    # Setup
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    processor = MarkdownProcessor(remove_unicode=True, remove_emoji=True)
    converter = WordConverter(output_dir)
    
    # Test content
    test_content = """# Test Document

This is a test document.

## Table Test
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

## Code Test
```python
print("Hello World")
```
"""
    
    # Process content
    processed_content = processor.process_content(test_content)
    
    # Convert to Word
    output_path = output_dir / "test_output.docx"
    success = converter.convert(processed_content, output_path)
    
    # Verify
    assert success
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    
    # Cleanup
    output_path.unlink(missing_ok=True)


def test_word_converter_with_file():
    """Test Word conversion with actual markdown file."""
    # Setup
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    processor = MarkdownProcessor(remove_unicode=True, remove_emoji=True)
    converter = WordConverter(output_dir)
    
    # Test file
    test_file = Path("tests/sample.md")
    assert test_file.exists(), "Sample markdown file not found"
    
    # Process file
    processed_content = processor.process_file(test_file)
    
    # Convert to Word
    output_path = output_dir / "sample_output.docx"
    success = converter.convert(processed_content, output_path)
    
    # Verify
    assert success
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    
    # Cleanup
    output_path.unlink(missing_ok=True)


def test_unicode_emoji_removal():
    """Test that unicode and emoji characters are removed."""
    processor = MarkdownProcessor(remove_unicode=True, remove_emoji=True)
    
    # Test content with unicode and emoji
    test_content = "Hello 🌍 World with unicode: café résumé"
    
    # Process content
    processed_content = processor.process_content(test_content)
    
    # Verify unicode and emoji are removed
    assert "🌍" not in processed_content
    assert "é" not in processed_content
    assert "Hello" in processed_content
    assert "World" in processed_content


if __name__ == "__main__":
    pytest.main([__file__])
