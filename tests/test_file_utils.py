# ./tests/test_file_utils.py

import os
import pytest
from summarizeit.fs.file_utils import compute_md5_hash, get_relative_path

@pytest.fixture
def temp_test_file(tmp_path):
    """Create a temporary test file with known content."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    return test_file

def test_compute_md5_hash(temp_test_file):
    """Test MD5 hash computation."""
    # Known MD5 hash for "test content"
    expected_hash = "9473fdd0d880a43c21b7778d34872157"
    
    computed_hash = compute_md5_hash(str(temp_test_file))
    assert computed_hash == expected_hash

def test_compute_md5_hash_empty_file(tmp_path):
    """Test MD5 hash computation for empty file."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    
    # Known MD5 hash for empty file
    expected_hash = "d41d8cd98f00b204e9800998ecf8427e"
    
    computed_hash = compute_md5_hash(str(empty_file))
    assert computed_hash == expected_hash

def test_get_relative_path(tmp_path):
    """Test relative path computation."""
    # Create nested directory structure
    nested_dir = tmp_path / "a" / "b" / "c"
    nested_dir.mkdir(parents=True)
    test_file = nested_dir / "test.txt"
    test_file.touch()
    
    rel_path = get_relative_path(str(test_file), str(tmp_path))
    expected_path = os.path.join("a", "b", "c", "test.txt")
    
    assert rel_path == expected_path

def test_get_relative_path_same_directory(tmp_path):
    """Test relative path when file is in root directory."""
    test_file = tmp_path / "test.txt"
    test_file.touch()
    
    rel_path = get_relative_path(str(test_file), str(tmp_path))
    assert rel_path == "test.txt"
