# ./tests/test_main.py

import os
import json
import pytest
from pathlib import Path
from summarizeit.main import main, DEFAULT_KV_FILENAME, DEFAULT_ALLOWEDLIST_FILENAME

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory with some test files."""
    # Create test files
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    
    # Create a Python file
    py_file = source_dir / "test.py"
    py_file.write_text("def hello(): return 'world'")
    
    # Create a JavaScript file
    js_file = source_dir / "test.js"
    js_file.write_text("function hello() { return 'world'; }")
    
    # Create some files that should be ignored
    (source_dir / ".git").mkdir()
    (source_dir / ".git" / "config").write_text("git config")
    
    return tmp_path

@pytest.fixture
def custom_allowedlist(temp_project_dir):
    """Create a custom allowedlist file."""
    allowedlist_path = temp_project_dir / DEFAULT_ALLOWEDLIST_FILENAME
    allowedlist_path.write_text("*.py\n*.js")
    return allowedlist_path

def test_main_creates_kv_store(temp_project_dir):
    """Test that main creates KV store if it doesn't exist."""
    main(str(temp_project_dir))
    
    kv_file = temp_project_dir / DEFAULT_KV_FILENAME
    assert kv_file.exists()
    
    # Check KV store contents
    with open(kv_file) as f:
        data = json.load(f)
    
    # Should have entries for test.py and test.js
    assert len(data) == 2
    assert any("test.py" in path for path in data.keys())
    assert any("test.js" in path for path in data.keys())

def test_main_skips_ignored_directories(temp_project_dir):
    """Test that main skips common directories that should be ignored."""
    main(str(temp_project_dir))
    
    kv_file = temp_project_dir / DEFAULT_KV_FILENAME
    with open(kv_file) as f:
        data = json.load(f)
    
    # Should not have any entries from .git directory
    assert not any(".git" in path for path in data.keys())

def test_main_uses_custom_allowedlist(temp_project_dir, custom_allowedlist):
    """Test that main respects custom allowedlist patterns."""
    # Add a file that's not in allowedlist
    cpp_file = temp_project_dir / "src" / "test.cpp"
    cpp_file.write_text("int main() { return 0; }")
    
    main(str(temp_project_dir))
    
    kv_file = temp_project_dir / DEFAULT_KV_FILENAME
    with open(kv_file) as f:
        data = json.load(f)
    
    # Should only have .py and .js files
    assert not any(".cpp" in path for path in data.keys())
    assert any(".py" in path for path in data.keys())
    assert any(".js" in path for path in data.keys())

def test_main_updates_changed_files(temp_project_dir):
    """Test that main updates files when they change."""
    # First run
    main(str(temp_project_dir))
    
    kv_file = temp_project_dir / DEFAULT_KV_FILENAME
    with open(kv_file) as f:
        initial_data = json.load(f)
    
    # Modify a file
    py_file = temp_project_dir / "src" / "test.py"
    py_file.write_text("def hello(): return 'changed'")
    
    # Second run
    main(str(temp_project_dir))
    
    with open(kv_file) as f:
        updated_data = json.load(f)
    
    # Hash should be different for the modified file
    py_file_key = next(key for key in updated_data.keys() if "test.py" in key)
    assert initial_data[py_file_key]["hash"] != updated_data[py_file_key]["hash"]

def test_main_preserves_external_ids(temp_project_dir):
    """Test that main preserves external IDs when updating files."""
    # First run
    main(str(temp_project_dir))
    
    kv_file = temp_project_dir / DEFAULT_KV_FILENAME
    with open(kv_file) as f:
        initial_data = json.load(f)
    
    # Modify a file
    py_file = temp_project_dir / "src" / "test.py"
    py_file.write_text("def hello(): return 'changed'")
    
    # Second run
    main(str(temp_project_dir))
    
    with open(kv_file) as f:
        updated_data = json.load(f)
    
    # External IDs should be preserved
    for key in initial_data:
        assert initial_data[key]["external_id"] == updated_data[key]["external_id"]
