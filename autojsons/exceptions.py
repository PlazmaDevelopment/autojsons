"""
Custom exceptions for the AutoJSONs module.
"""


class JSONError(Exception):
    """Base exception for all JSON-related errors."""
    pass


class JSONFileError(JSONError):
    """
    Raised when there's an error related to file operations.
    
    This could be due to file not found, permission issues, or other I/O errors.
    """
    pass


class JSONValidationError(JSONError):
    """
    Raised when JSON data fails validation.
    
    This could be due to invalid JSON syntax, missing required fields,
    or data that doesn't match the expected schema.
    """
    pass
