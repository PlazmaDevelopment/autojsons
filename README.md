# AutoJSONs

A Python module for easy JSON file handling. This module provides a simple and intuitive interface for reading, writing, updating, and managing JSON files with automatic file handling.

## Installation

```bash
pip install autojsons
```

## Features

- Read and write JSON files with a single function call
- Automatically handle file creation and directory structure
- Update existing JSON files with new data
- Check if a JSON file exists and is valid
- Recursively load all JSON files from a directory
- Comprehensive error handling with custom exceptions

## Usage

### Basic Usage

```python
import autojsons

# Create a new JSON file
autojsons.create('data.json', {"name": "John", "age": 30})

# Read a JSON file
data = autojsons.read('data.json')
print(data)  # {'name': 'John', 'age': 30}

# Update a JSON file
autojsons.update('data.json', {"age": 31, "city": "New York"})

# Read all JSON files in a directory
all_data = autojsons.auto('path/to/json/files')

# Check if a JSON file exists
if autojsons.exists('data.json'):
    print("File exists!")

# Delete a JSON file
autojsons.delete('data.json')
```

### Advanced Usage

```python
import autojsons

# Write with custom indentation and encoding
autojsons.write(
    'config.json',
    {"debug": True, "max_retries": 5},
    indent=2,
    ensure_ascii=False
)

# Update a file, creating it if it doesn't exist
autojsons.update('new_file.json', {"key": "value"}, create_if_not_exists=True)

# Create a file only if it doesn't exist
autojsons.create('config.json', {"theme": "dark"}, overwrite=False)
```

## API Reference

### Functions

#### `auto(directory='.', recursive=True, create_if_not_exists=False)`
Load all JSON files from a directory.

#### `read(file_path)`
Read and parse a JSON file.

#### `write(file_path, data, indent=4, ensure_ascii=False, create_dirs=True)`
Write data to a JSON file.

#### `update(file_path, updates, create_if_not_exists=False)`
Update a JSON file with new data.

#### `delete(file_path)`
Delete a JSON file.

#### `create(file_path, data=None, overwrite=False, indent=4, ensure_ascii=False)`
Create a new JSON file with optional initial data.

#### `exists(file_path)`
Check if a JSON file exists and is valid.

### Exceptions

- `JSONError`: Base exception for all JSON-related errors
- `JSONFileError`: Raised for file-related errors
- `JSONValidationError`: Raised for JSON validation errors

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
