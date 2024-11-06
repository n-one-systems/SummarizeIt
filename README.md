# SummarizeIt

![SummarizeIt Logo](https://github.com/n-one-systems/SummarizeIt/blob/5783238ba2f0826753d62317f6389e4117297445/assets/logo_small.png)

**Version 0.2.0**

SummarizeIt is a Python tool designed to create and maintain documentation indices for your codebase. It traverses directories to build a key-value (KV) store containing file metadata, hashes, and high-level documentation summaries. This helps teams maintain an up-to-date overview of their project's structure and content.

## Features

- **Intelligent Directory Traversal**: Recursively processes files while following an allowedlist approach
- **Change Detection**: Uses MD5 hashing to identify modified files
- **Persistent File Tracking**: Maintains unique IDs for files even when they move or change
- **Documentation Generation**: Creates high-level documentation summaries for code files
- **Flexible Allowedlist Rules**: Uses `.summarizeitallowedlist` to specify which files to process
- **Default Language Support**: Built-in support for common programming languages (Python, JavaScript, TypeScript, Go, Java, Ruby, PHP, Rust)
- **Python 3.12+**: Takes advantage of modern Python features

## Installation

```bash

# install from source
git clone https://github.com/n-one-systems/SummarizeIt.git
cd SummarizeIt
pip install .
```

## Usage

### Command Line

```bash
# Using the installed package
summarizeit

# The tool will:
# - Use current directory as root
# - Create summarizeit.json in the root directory
# - Use default allowedlist patterns if no .summarizeitallowedlist is found
```

### Programmatic Usage

```python
from summarizeit import main

# Process current directory with default settings
main()

# Process specific directory with custom KV store location
main("./my_project", "./docs/summarizeit.json")
```

## Configuration

### Allowedlist Rules (`.summarizeitallowedlist`)

Create a `.summarizeitallowedlist` file in your project root to specify which files to process. If no file is present, these default patterns are used:

```
*.py    # Python files
*.js    # JavaScript files
*.jsx   # React files
*.ts    # TypeScript files
*.tsx   # TypeScript React files
*.go    # Go files
*.java  # Java files
*.rb    # Ruby files
*.php   # PHP files
*.rs    # Rust files
```

Special features:
- Supports glob patterns (`*`, `?`, `[]`)
- Comments start with `#`
- Empty lines are ignored
- Custom patterns can be added to process additional file types

## KV Store Format

The tool generates a JSON file with the following structure:

```json
{
    "path/to/file.py": {
        "hash": "md5_hash_of_file",
        "external_id": "unique_uuid",
        "high_level_documentation": "File documentation summary"
    }
}
```

## Default Exclusions

The following directories are automatically excluded:
- `.git`
- `__pycache__`
- `node_modules`
- `venv`
- `.venv`

## Development

### Requirements
- Python 3.12 or higher
- hatchling (for building)

### Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest
```

### Project Structure

```
summarizeit/
├── src/
│   └── summarizeit/
│       ├── __init__.py
│       ├── main.py
│       ├── fs/
│       │   ├── __init__.py
│       │   ├── file_utils.py
│       │   └── allowed_list.py
│       ├── storage/
│       │   ├── __init__.py
│       │   └── kv_store.py
│       └── docs/
│           ├── __init__.py
│           └── generator.py
├── tests/
├── pyproject.toml
└── README.md
```

## License

AGPLv3 License - See LICENSE file for details.

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Contact

For bugs, questions, and discussions please use the [GitHub Issues](https://github.com/n-one-systems/SummarizeIt/issues).

---
Developed with ♥ by [N-ONE!](https://github.com/n-one-systems)
