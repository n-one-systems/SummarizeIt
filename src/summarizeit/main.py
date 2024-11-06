# ./src/summarizeit/main.py

import os
from typing import Optional
from .storage.kv_store import KVStore
from .fs.file_utils import compute_md5_hash, get_relative_path
from .fs.allowed_list import AllowedlistHandler
from .docs.generator import get_code_file_documentation

DEFAULT_KV_FILENAME = 'summarizeit.json'
DEFAULT_ALLOWEDLIST_FILENAME = '.summarizeitallowedlist'

def main(root_dir: Optional[str] = None, kv_file_path: Optional[str] = None) -> None:
    """
    Main function to process and index files in the given directory.

    Args:
        root_dir (str, optional): Root directory to process. Defaults to current directory.
        kv_file_path (str, optional): Path to the KV store file. Defaults to 'summarizeit.json' in root_dir.
    """
    # Set defaults
    if root_dir is None:
        root_dir = os.getcwd()
    
    if kv_file_path is None:
        kv_file_path = os.path.join(root_dir, DEFAULT_KV_FILENAME)

    # Initialize KV store
    kv_store = KVStore(kv_file_path)
    
    # Initialize allowedlist handler
    allowedlist_path = os.path.join(root_dir, DEFAULT_ALLOWEDLIST_FILENAME)
    allowedlist = AllowedlistHandler(allowedlist_path)
    
    # Print current patterns being used
    print("Using allowedlist patterns:", ", ".join(sorted(allowedlist.get_patterns())))

    # Walk through directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip common non-code directories by default
        dirnames[:] = [d for d in dirnames if d not in {'.git', '__pycache__', 'node_modules', 'venv', '.venv'}]
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = get_relative_path(file_path, root_dir)

            # Skip if file doesn't match allowedlist
            if not allowedlist.should_include(rel_path):
                continue

            # Skip the KV file itself
            if os.path.abspath(file_path) == os.path.abspath(kv_file_path):
                continue

            file_hash = compute_md5_hash(file_path)
            
            # Process file if it's new or changed
            if kv_store.has_changed(rel_path, file_hash):
                print(f"Processing: {rel_path}")
                high_level_doc = get_code_file_documentation(file_path)
                kv_store.update_file_entry(rel_path, file_hash, high_level_doc)

    # Save changes
    kv_store.save()
    print(f"KV store updated and saved to {kv_file_path}")

def cli():
    """Command line interface entry point"""
    main()

if __name__ == "__main__":
    cli()
