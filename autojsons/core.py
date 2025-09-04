"""
Core functionality for AutoJSONs module.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .exceptions import JSONError, JSONFileError, JSONValidationError


def auto(directory: str = '.', recursive: bool = True, create_if_not_exists: bool = False) -> Dict[str, Any]:
    """
    Automatically load all JSON files in the specified directory.
    
    Args:
        directory: Directory path to search for JSON files (default: current directory)
        recursive: Whether to search subdirectories (default: True)
        create_if_not_exists: Create the directory if it doesn't exist (default: False)
        
    Returns:
        Dict containing file names (without extension) as keys and their parsed content as values
        
    Raises:
        JSONFileError: If the directory doesn't exist and create_if_not_exists is False
    """
    directory = Path(directory)
    
    if not directory.exists():
        if create_if_not_exists:
            directory.mkdir(parents=True, exist_ok=True)
            return {}
        raise JSONFileError(f"Directory not found: {directory}")
    
    pattern = '**/*.json' if recursive else '*.json'
    result = {}
    
    for json_file in directory.glob(pattern):
        if json_file.is_file():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    result[json_file.stem] = json.load(f)
            except json.JSONDecodeError as e:
                raise JSONError(f"Error decoding JSON file {json_file}: {str(e)}")
            except Exception as e:
                raise JSONFileError(f"Error reading file {json_file}: {str(e)}")
    
    return result


def read(file_path: Union[str, Path]) -> Any:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        JSONFileError: If the file doesn't exist or can't be read
        JSONError: If the file contains invalid JSON
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise JSONFileError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise JSONError(f"Invalid JSON in file {file_path}: {str(e)}")
    except Exception as e:
        raise JSONFileError(f"Error reading file {file_path}: {str(e)}")


def write(file_path: Union[str, Path], data: Any, indent: int = 4, ensure_ascii: bool = False, 
          create_dirs: bool = True) -> None:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Data to be written (must be JSON-serializable)
        indent: Number of spaces for indentation (default: 4)
        ensure_ascii: If True, escape non-ASCII characters (default: False)
        create_dirs: Create parent directories if they don't exist (default: True)
        
    Raises:
        JSONError: If data is not JSON-serializable
        JSONFileError: If there's an error writing to the file
    """
    file_path = Path(file_path)
    
    if create_dirs and not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    except (TypeError, OverflowError, ValueError) as e:
        raise JSONError(f"Data is not JSON-serializable: {str(e)}")
    except Exception as e:
        raise JSONFileError(f"Error writing to file {file_path}: {str(e)}")


def update(file_path: Union[str, Path], updates: Dict[str, Any], create_if_not_exists: bool = False) -> Dict[str, Any]:
    """
    Update a JSON file with new data.
    
    Args:
        file_path: Path to the JSON file
        updates: Dictionary with updates to apply
        create_if_not_exists: Create the file if it doesn't exist (default: False)
        
    Returns:
        Updated data
        
    Raises:
        JSONFileError: If the file doesn't exist and create_if_not_exists is False
        JSONError: If there's an error reading or writing the file
    """
    file_path = Path(file_path)
    
    if file_path.exists():
        data = read(file_path)
        if not isinstance(data, dict):
            data = {}
    elif create_if_not_exists:
        data = {}
    else:
        raise JSONFileError(f"File not found: {file_path}")
    
    data.update(updates)
    write(file_path, data)
    return data


def delete(file_path: Union[str, Path]) -> bool:
    """
    Delete a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        bool: True if the file was deleted, False if it didn't exist
        
    Raises:
        JSONFileError: If there's an error deleting the file
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False
    
    try:
        file_path.unlink()
        return True
    except Exception as e:
        raise JSONFileError(f"Error deleting file {file_path}: {str(e)}")


def create(file_path: Union[str, Path], data: Optional[Any] = None, overwrite: bool = False, 
          indent: int = 4, ensure_ascii: bool = False) -> bool:
    """
    Create a new JSON file with optional initial data.
    
    Args:
        file_path: Path to the new JSON file
        data: Initial data (default: empty dict)
        overwrite: Overwrite the file if it exists (default: False)
        indent: Number of spaces for indentation (default: 4)
        ensure_ascii: If True, escape non-ASCII characters (default: False)
        
    Returns:
        bool: True if the file was created, False if it already exists and overwrite is False
        
    Raises:
        JSONFileError: If the file already exists and overwrite is False
        JSONError: If there's an error creating or writing to the file
    """
    file_path = Path(file_path)
    
    if file_path.exists() and not overwrite:
        return False
    
    if data is None:
        data = {}
    
    write(file_path, data, indent=indent, ensure_ascii=ensure_ascii, create_dirs=True)
    return True


def exists(file_path: Union[str, Path]) -> bool:
    """
    Check if a JSON file exists and is valid.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        bool: True if the file exists and contains valid JSON, False otherwise
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, Exception):
        return False
