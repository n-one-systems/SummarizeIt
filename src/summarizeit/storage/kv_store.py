# ./src/summarizeit/storage/kv_store.py

import os
import json
import uuid
from typing import Dict, Any

class KVStore:
    def __init__(self, kv_file_path: str):
        self.kv_file_path = kv_file_path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """
        Load the KV store from a JSON file.

        Returns:
            dict: The KV data.
        """
        if os.path.exists(self.kv_file_path):
            with open(self.kv_file_path, 'r') as f:
                return json.load(f)
        return {}

    def save(self):
        """Save the KV data to the JSON file."""
        with open(self.kv_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_file_entry(self, rel_path: str, file_hash: str, high_level_doc: str) -> None:
        """
        Update or create an entry for a file in the KV store.

        Args:
            rel_path (str): Relative path of the file
            file_hash (str): MD5 hash of the file
            high_level_doc (str): Generated documentation for the file
        """
        if rel_path not in self.data:
            external_id = str(uuid.uuid4())
        else:
            external_id = self.data[rel_path]['external_id']

        self.data[rel_path] = {
            'hash': file_hash,
            'external_id': external_id,
            'high_level_documentation': high_level_doc
        }

    def has_changed(self, rel_path: str, file_hash: str) -> bool:
        """
        Check if a file has changed since last indexing.

        Args:
            rel_path (str): Relative path of the file
            file_hash (str): Current MD5 hash of the file

        Returns:
            bool: True if the file is new or has changed, False otherwise
        """
        return rel_path not in self.data or self.data[rel_path]['hash'] != file_hash
