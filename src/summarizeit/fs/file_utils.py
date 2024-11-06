# ./src/summarizeit/fs/file_utils.py

import os
import hashlib

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

def get_relative_path(file_path, root_dir):
    """
    Get the relative path of a file from the root directory.

    Args:
        file_path (str): The absolute path to the file
        root_dir (str): The root directory path

    Returns:
        str: The relative path from root_dir to file_path
    """
    return os.path.relpath(file_path, root_dir)
