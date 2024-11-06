# ./src/summarizeit/fs/allowed_list.py

import os
import fnmatch
from typing import List, Set

DEFAULT_PATTERNS = [
    '*.py',    # Python files
    '*.js',    # JavaScript files
    '*.jsx',   # React files
    '*.ts',    # TypeScript files
    '*.tsx',   # TypeScript React files
    '*.go',    # Go files
    '*.java',  # Java files
    '*.rb',    # Ruby files
    '*.php',   # PHP files
    '*.rs',    # Rust files
]

class AllowedlistHandler:
    """Handles file allowedlisting based on patterns"""
    
    def __init__(self, allowedlist_file_path: str = None):
        """
        Initialize the allowedlist handler.
        
        Args:
            allowedlist_file_path (str, optional): Path to .summarizeitallowedlist file
        """
        self.patterns = self._load_patterns(allowedlist_file_path)

    def _load_patterns(self, allowedlist_file_path: str) -> Set[str]:
        """
        Load allowedlist patterns from file or use defaults.
        
        Args:
            allowedlist_file_path (str): Path to the allowedlist file
            
        Returns:
            Set[str]: Set of allowedlist patterns
        """
        patterns = set()
        
        # Try to load from file if it exists
        if allowedlist_file_path and os.path.exists(allowedlist_file_path):
            with open(allowedlist_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.add(line)
        
        # If no patterns were loaded, use defaults
        if not patterns:
            patterns.update(DEFAULT_PATTERNS)
            
        return patterns
    
    def should_include(self, path: str) -> bool:
        """
        Check if a file should be included based on allowedlist patterns.
        
        Args:
            path (str): The path to check
            
        Returns:
            bool: True if the file should be included
        """
        # Normalize path separators to forward slashes
        path = path.replace(os.sep, '/')
        filename = os.path.basename(path)
        
        return any(fnmatch.fnmatch(filename, pattern) for pattern in self.patterns)

    def get_patterns(self) -> Set[str]:
        """
        Get the current allowedlist patterns.
        
        Returns:
            Set[str]: Current allowedlist patterns
        """
        return self.patterns.copy()
