# ./tests/test_kv_store.py

import os
import json
import pytest
from summarizeit.storage.kv_store import KVStore

@pytest.fixture
def temp_kv_file(tmp_path):
    """Create a temporary KV store file."""
    return tmp_path / "test_store.json"

@pytest.fixture
def kv_store(temp_kv_file):
    """Create a KV store instance."""
    return KVStore(str(temp_kv_file))

def test_kv_store_creation(temp_kv_file):
    """Test KV store initialization."""
    store = KVStore(str(temp_kv_file))
    assert not temp_kv_file.exists()  # File should not be created until save
    assert store.data == {}

def test_kv_store_save_and_load(kv_store, temp_kv_file):
    """Test saving and loading KV store."""
    # Add some data
    kv_store.update_file_entry("test.py", "hash123", "Test documentation")
    kv_store.save()
    
    # Load in new instance
    new_store = KVStore(str(temp_kv_file))
    assert "test.py" in new_store.data
    assert new_store.data["test.py"]["hash"] == "hash123"
    assert new_store.data["test.py"]["high_level_documentation"] == "Test documentation"

def test_kv_store_update_preserves_external_id(kv_store):
    """Test that updating a file preserves its external ID."""
    # Initial entry
    kv_store.update_file_entry("test.py", "hash1", "Doc 1")
    initial_id = kv_store.data["test.py"]["external_id"]
    
    # Update same file
    kv_store.update_file_entry("test.py", "hash2", "Doc 2")
    assert kv_store.data["test.py"]["external_id"] == initial_id
    assert kv_store.data["test.py"]["hash"] == "hash2"
    assert kv_store.data["test.py"]["high_level_documentation"] == "Doc 2"

def test_kv_store_has_changed(kv_store):
    """Test file change detection."""
    kv_store.update_file_entry("test.py", "hash1", "Doc")
    
    assert kv_store.has_changed("test.py", "hash2")  # Different hash
    assert not kv_store.has_changed("test.py", "hash1")  # Same hash
    assert kv_store.has_changed("new.py", "hash1")  # New file
