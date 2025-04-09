"""
Functions for processing boolean values from various string representations.

This module provides utilities for converting various string representations to boolean
values, with support for custom true/false value sets.
"""

from typing import Any, Optional, Set

TRUE_CHOICES = {"on", "1", "true", "yes", "==true=="}
"""
Standard string values that represent True.
"""

FALSE_CHOICES = {"off", "0", "false", "no", "==false=="}
"""
Standard string values that represent False.
"""

StrChoices = Set[str]


def make_boolean(
    true_choices: Optional[StrChoices] = None, false_choices: Optional[StrChoices] = None
):
    """
    Create a boolean converter function with custom true/false choices.
    
    This function returns a new function that converts values to booleans
    using the specified sets of strings that represent true and false.
    
    :param true_choices: Set of strings to interpret as True
    :param false_choices: Set of strings to interpret as False
    :return: A function that converts values to booleans
    """
    def _inner(value):
        return boolean(value, true_choices, false_choices)

    return _inner


def boolean(
    value: Any,
    true_choices: Optional[StrChoices] = None,
    false_choices: Optional[StrChoices] = None,
) -> bool:
    """
    Convert a value to a boolean.
    
    If the value is a string, it is converted based on membership in the
    true_choices or false_choices sets. Non-string values are converted
    using Python's built-in bool() function.

    .. note::
        The function is case-insensitive and ignores leading/trailing whitespace.
    
    :param value: The value to convert to a boolean
    :param true_choices: Set of strings to interpret as True
    :param false_choices: Set of strings to interpret as False
    :return: The boolean representation of the value
    :raises ValueError: If the value is a string but not in either set of choices
    """
    if true_choices is None:
        true_choices = TRUE_CHOICES
    if false_choices is None:
        false_choices = FALSE_CHOICES

    if isinstance(value, str):
        _value = value.strip().lower()
        if _value in true_choices:
            return True
        if _value in false_choices:
            return False
        raise ValueError(
            f"unexpected value: {value}, expected choices:"
            f" {str(true_choices.union(false_choices))}"
        )
    return bool(value)
