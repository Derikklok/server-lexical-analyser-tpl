# app/services/string_operations.py

def remove_whitespace(input_str: str) -> str:
    """Removes all whitespace characters."""
    return input_str.replace(" ", "")