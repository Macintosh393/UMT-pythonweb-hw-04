# Async Directory Sorter

A Python utility that recursively explores a source directory and sorts files into a target directory based on their file extensions using asynchronous I/O.

## Features

- **Asynchronous Execution**: Uses `asyncio`, `aiopath`, and `aioshutil` for high-performance file operations.
- **Recursive Sorting**: Automatically traverses nested directories.
- **Extension-based Organization**: Files are grouped into folders named after their extensions (e.g., `.jpg` files go into a `jpg/` folder).
- **Robust Error Handling**: Handles missing directories, permission issues, and corrupted files gracefully with logging.

## Requirements

- Python 3.12 (specifically optimized for 3.12 to ensure `aiopath` compatibility)
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd UMT-pythonweb-hw-04
   ```

2. Sync the environment and dependencies using `uv`:
   ```bash
   uv sync
   ```

## Usage

Run the script using `uv run`, providing the source and output directories as arguments:

```bash
uv run main.py <source_directory> <output_directory>
```

### Example

```bash
uv run main.py ./my_downloads ./sorted_files
```

If the `output_directory` does not exist, the program will create it automatically.

## How it Works

1. **Scan**: The program scans the source directory recursively.
2. **Sort**: It creates a subfolder in the destination named after the file extension (without the dot).
3. **Copy**: Files are copied asynchronously to their new locations.

## Logging

The program logs errors (like permission issues or read failures) to the console using the standard `logging` module. Success messages are printed upon completion.
