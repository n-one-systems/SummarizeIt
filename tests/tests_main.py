import pytest
import os
import json
import tempfile
import shutil
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from summarizeit.main import (
    compute_md5_hash,
    load_kv_store,
    save_kv_store,
    load_ignore_patterns,
    should_ignore,
    main
)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    # Create test files
    test_file1 = os.path.join(temp_dir, "test1.py")
    test_file2 = os.path.join(temp_dir, "test2.py")
    
    with open(test_file1, 'w') as f:
        f.write("print('test1')")
    with open(test_file2, 'w') as f:
        f.write("print('test2')")
    
    return temp_dir, test_file1, test_file2

@pytest.fixture
def ignore_file(temp_dir):
    """Create a sample .ignoreindexing file."""
    ignore_path = os.path.join(temp_dir, ".ignoreindexing")
    with open(ignore_path, 'w') as f:
        f.write("*.pyc\n")
        f.write("__pycache__\n")
        f.write("# Comment line\n")
        f.write("ignored_dir/*\n")
    return ignore_path

@pytest.fixture
def kv_store_file(temp_dir):
    """Create a sample KV store file."""
    kv_path = os.path.join(temp_dir, "kv_store.json")
    initial_data = {
        "test1.py": {
            "hash": "dummy_hash",
            "external_id": "dummy_uuid",
            "high_level_documentation": "Test file 1"
        }
    }
    with open(kv_path, 'w') as f:
        json.dump(initial_data, f)
    return kv_path

def test_compute_md5_hash(sample_files):
    """Test MD5 hash computation."""
    _, test_file1, _ = sample_files
    hash1 = compute_md5_hash(test_file1)
    
    # Test if hash changes when file content changes
    with open(test_file1, 'w') as f:
        f.write("modified content")
    hash2 = compute_md5_hash(test_file1)
    
    assert isinstance(hash1, str)
    assert len(hash1) == 32  # MD5 hash is 32 characters
    assert hash1 != hash2  # Hashes should be different for different content

def test_load_kv_store(kv_store_file):
    """Test loading KV store."""
    data = load_kv_store(kv_store_file)
    assert isinstance(data, dict)
    assert "test1.py" in data
    assert data["test1.py"]["hash"] == "dummy_hash"
    
    # Test loading non-existent file
    non_existent = os.path.join(os.path.dirname(kv_store_file), "non_existent.json")
    empty_data = load_kv_store(non_existent)
    assert isinstance(empty_data, dict)
    assert len(empty_data) == 0

def test_save_kv_store(temp_dir):
    """Test saving KV store."""
    test_data = {"test": {"hash": "123", "external_id": "456"}}
    kv_path = os.path.join(temp_dir, "test_kv.json")
    
    save_kv_store(kv_path, test_data)
    assert os.path.exists(kv_path)
    
    # Verify saved data
    with open(kv_path, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == test_data

def test_load_ignore_patterns(ignore_file):
    """Test loading ignore patterns."""
    patterns = load_ignore_patterns(ignore_file)
    assert isinstance(patterns, list)
    assert "*.pyc" in patterns
    assert "__pycache__" in patterns
    assert "# Comment line" not in patterns
    assert "ignored_dir/*" in patterns
    
    # Test with non-existent file
    non_existent = os.path.join(os.path.dirname(ignore_file), "non_existent")
    empty_patterns = load_ignore_patterns(non_existent)
    assert isinstance(empty_patterns, list)
    assert len(empty_patterns) == 0

def test_should_ignore():
    """Test ignore pattern matching."""
    patterns = ["*.pyc", "__pycache__", "ignored_dir/*"]
    
    assert should_ignore("test.pyc", patterns) == True
    assert should_ignore("__pycache__/test.py", patterns) == True
    assert should_ignore("ignored_dir/file.txt", patterns) == True
    assert should_ignore("test.py", patterns) == False
    assert should_ignore("src/test.py", patterns) == False

def test_main_integration(temp_dir, sample_files, ignore_file):
    """Test the main function integration."""
    kv_path = os.path.join(temp_dir, "kv_store.json")
    
    # Create an ignored file that shouldn't be processed
    ignored_dir = os.path.join(temp_dir, "ignored_dir")
    os.makedirs(ignored_dir)
    with open(os.path.join(ignored_dir, "ignored.py"), 'w') as f:
        f.write("print('ignored')")
    
    # Run main function
    main(temp_dir, kv_path)
    
    # Verify KV store was created and contains expected files
    assert os.path.exists(kv_path)
    with open(kv_path, 'r') as f:
        kv_data = json.load(f)
    
    # Check that test files are in KV store
    assert "test1.py" in kv_data
    assert "test2.py" in kv_data
    
    # Check that ignored file is not in KV store
    assert "ignored_dir/ignored.py" not in kv_data
    
    # Verify structure of entries
    for entry in kv_data.values():
        assert "hash" in entry
        assert "external_id" in entry
        assert "high_level_documentation" in entry

if __name__ == "__main__":
    pytest.main([__file__])
