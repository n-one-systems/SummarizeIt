# ./tests/test_allowed_list.py

import pytest
from pathlib import Path
from summarizeit.fs.allowed_list import AllowedlistHandler, DEFAULT_PATTERNS

@pytest.fixture
def temp_allowedlist_file(tmp_path):
    """Create a temporary allowedlist file."""
    return tmp_path / ".summarizeitallowedlist"

def test_allowedlist_defaults():
    """Test default patterns when no file exists."""
    handler = AllowedlistHandler(None)
    patterns = handler.get_patterns()
    
    assert patterns == set(DEFAULT_PATTERNS)
    assert handler.should_include("test.py")
    assert handler.should_include("test.js")
    assert not handler.should_include("test.txt")

def test_allowedlist_custom_patterns(temp_allowedlist_file):
    """Test loading custom patterns from file."""
    # Create allowedlist with custom patterns
    temp_allowedlist_file.write_text("*.txt\n*.md")
    
    handler = AllowedlistHandler(str(temp_allowedlist_file))
    patterns = handler.get_patterns()
    
    assert patterns == {"*.txt", "*.md"}
    assert handler.should_include("test.txt")
    assert handler.should_include("test.md")
    assert not handler.should_include("test.py")

def test_allowedlist_empty_file(temp_allowedlist_file):
    """Test behavior with empty allowedlist file."""
    temp_allowedlist_file.write_text("")
    
    handler = AllowedlistHandler(str(temp_allowedlist_file))
    patterns = handler.get_patterns()
    
    # Should fall back to defaults
    assert patterns == set(DEFAULT_PATTERNS)

def test_allowedlist_comments(temp_allowedlist_file):
    """Test that comments in allowedlist file are ignored."""
    content = """
    # Python files
    *.py
    # JavaScript files
    *.js
    """
    temp_allowedlist_file.write_text(content)
    
    handler = AllowedlistHandler(str(temp_allowedlist_file))
    patterns = handler.get_patterns()
    
    assert patterns == {"*.py", "*.js"}

def test_allowedlist_path_normalization():
    """Test that path separators are handled correctly."""
    handler = AllowedlistHandler(None)
    
    # Should work with both forward and backward slashes
    assert handler.should_include("path/to/test.py")
    assert handler.should_include("path\\to\\test.py")
