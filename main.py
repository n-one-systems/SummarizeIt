import os
import hashlib
import uuid
import json
import fnmatch

def get_code_file_documentation(path_of_file: str, programming_language: str = 'python') -> str:
    """
    Generate a short summary of the code snippet.

    Args:
        path_of_file (str): The path to the code file.
        programming_language (str, optional): The programming language of the code file.

    Returns:
        str: A short summary of the code.
    """
    # Placeholder for actual implementation
    return f"Summary of {os.path.basename(path_of_file)}"

def compute_md5_hash(file_path):
    """
    Compute the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_kv_store(kv_file_path):
    """
    Load the KV store from a JSON file.

    Args:
        kv_file_path (str): The path to the KV store file.

    Returns:
        dict: The KV data.
    """
    if os.path.exists(kv_file_path):
        with open(kv_file_path, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_kv_store(kv_file_path, kv_data):
    """
    Save the KV data to a JSON file.

    Args:
        kv_file_path (str): The path to the KV store file.
        kv_data (dict): The KV data to save.
    """
    with open(kv_file_path, 'w') as f:
        json.dump(kv_data, f, indent=4)

def load_ignore_patterns(ignore_file_path):
    """
    Load ignore patterns from the .ignoreindexing file.

    Args:
        ignore_file_path (str): The path to the .ignoreindexing file.

    Returns:
        list: A list of ignore patterns.
    """
    patterns = []
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def should_ignore(path, ignore_patterns):
    """
    Check if a path should be ignored based on the ignore patterns.

    Args:
        path (str): The path to check.
        ignore_patterns (list): A list of ignore patterns.

    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def main(root_dir, kv_file_path):
    kv_data = load_kv_store(kv_file_path)
    updated_kv_data = kv_data.copy()
    ignore_file_path = os.path.join(root_dir, '.ignoreindexing')
    ignore_patterns = load_ignore_patterns(ignore_file_path)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip ignored directories
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), root_dir), ignore_patterns)]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)

            # Skip files that match ignore patterns
            if should_ignore(rel_path, ignore_patterns):
                continue

            # Skip the KV file itself to avoid processing it
            if os.path.abspath(file_path) == os.path.abspath(kv_file_path):
                continue

            file_hash = compute_md5_hash(file_path)
            # Check if file is new or has changed
            if rel_path not in kv_data or kv_data[rel_path]['hash'] != file_hash:
                # Generate new UUID if file is new
                external_id = kv_data.get(rel_path, {}).get('external_id', str(uuid.uuid4()))
                high_level_doc = get_code_file_documentation(file_path)
                updated_kv_data[rel_path] = {
                    'hash': file_hash,
                    'external_id': external_id,
                    'high_level_documentation': high_level_doc
                }
    # Save updated KV data
    save_kv_store(kv_file_path, updated_kv_data)
    print(f"KV store updated and saved to {kv_file_path}")

if __name__ == "__main__":
    root_directory = '.'  # Replace with your project root directory
    kv_store_file = 'kv_store.json'  # KV store file name
    main(root_directory, kv_store_file)

