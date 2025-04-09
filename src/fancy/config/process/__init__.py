"""
Utilities for processing configuration values.

This module provides functions for converting and validating configuration values
according to type specifications. It includes handlers for various types of values:

- boolean: Convert various string representations to boolean values
- config: Process nested configuration objects
- config_list: Process lists of configuration objects
- flag_string/flag_container: Handle flag-based configuration
- auto_process_typ: Automatically select the appropriate processor
- auto_process_value: Convert values based on their type
- identical: Pass values through unchanged
"""

__all__ = [
    "boolean",
    "config",
    "config_list",
    "flag_string",
    "flag_container",
    "auto_process_typ",
    "auto_process_value",
    "identical"
]

from .boolean import boolean, make_boolean
from .config import config
from .config_list import config_list
from .flag_string import flag_string
from .flag_container import flag_container
from .auto_process_typ import auto_process_typ
from .auto_process_value import auto_process_value
from .identical import identical
