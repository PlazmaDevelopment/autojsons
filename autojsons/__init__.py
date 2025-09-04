"""
AutoJSONs - A Python module for easy JSON file handling.

This module provides a simple and intuitive interface for reading, writing,
updating, and managing JSON files with automatic file handling.
"""

from .core import auto, read, write, update, delete, create, exists
from .exceptions import JSONError, JSONFileError, JSONValidationError

__version__ = '0.1.0'
__all__ = [
    'auto',
    'read',
    'write',
    'update',
    'delete',
    'create',
    'exists',
    'JSONError',
    'JSONFileError',
    'JSONValidationError'
]
