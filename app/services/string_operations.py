# app/services/string_operations.py
import re

def remove_whitespace(input_str: str) -> str:
    """Removes all whitespace characters (spaces, tabs, newlines)."""
    return re.sub(r'\s+', '', input_str)