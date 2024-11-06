# SummarizeIt

![SummarizeIt Logo](https://github.com/n-one-systems/SummarizeIt/assets/logo.png)

**Version 0.1.0**

SummarizeIt is a lightweight Python tool that traverses a directory and creates a key-value (KV) index of files, providing useful metadata such as MD5 hashes, unique IDs, and concise documentation summaries for each code file. It aims to help developers maintain a consistent overview of their projects, identifying changes and keeping up-to-date with high-level documentation for each file.

## Features

- **Directory Traversal**: Recursively indexes all files in a given directory and subdirectories.
- **File Hashing**: Computes an MD5 hash for each file to detect changes.
- **UUID Generation**: Generates a unique external ID for each indexed file.
- **Automatic Summarization**: Uses the `get_code_file_documentation()` function to create brief summaries for code files.
- **Ignore Indexing Rules**: Supports `.ignoreindexing` file to exclude files or directories from indexing, similar to `.gitignore`.
- **Local Storage**: Stores KV information in a local JSON file for easy retrieval and update.

## Installation

To install SummarizeIt, clone the repository and ensure you have Python 3 installed:

```bash
# Clone the repository
git clone https://github.com/n-one-systems/SummarizeIt.git

# Change to the project directory
cd SummarizeIt

# Install required dependencies (if any)
pip install -r requirements.txt
```

## Usage

To index a directory, run the `main.py` script:

```bash
python main.py [root_directory] [kv_store_file]
```

### Arguments:

- **root_directory**: The root directory of your project (defaults to the current directory if not provided).
- **kv_store_file**: The file where the KV store will be saved (e.g., `kv_store.json`).

Example usage:

```bash
python main.py . kv_store.json
```

## Ignore Indexing Rules

SummarizeIt supports ignoring certain files and directories using an `.ignoreindexing` file. Add patterns to this file to specify files and directories that should be excluded from indexing.

### Example `.ignoreindexing` File:

```
# Ignore all text files
*.txt

# Ignore the build directory
build/

# Ignore all log files in the logs directory
logs/*
```

## How It Works

1. **Traverse Directory**: SummarizeIt traverses the root directory and its subdirectories.
2. **Generate KV Data**: For each file, it calculates an MD5 hash, generates a UUID, and creates a documentation summary.
3. **Store KV Data**: The data is stored in a JSON file for easy management and updates.
4. **Update Changes**: Only new or modified files are updated in the KV store.

## License

SummarizeIt is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

If you have any questions or suggestions, feel free to open an issue on GitHub.

## Roadmap

- **Version 0.2.0**: Planned support for multi-language code summaries and improved performance for large directories.

## Acknowledgments

This project is proudly developed by [N-One Systems](https://github.com/n-one-systems) to make code documentation and indexing simpler for developers.

## Contact
Please open an Issue 
