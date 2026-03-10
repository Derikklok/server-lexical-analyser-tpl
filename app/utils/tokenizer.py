# app/utils/tokenizer.py
import re

def tokenize_string(input_str: str):
    """Tokenizes the string using regular expressions."""
    
    token_specification = [
        ("NUMBER", r"\d+"),         # Integer
        ("ASSIGN", r"="),           # Assignment operator
        ("PLUS", r"\+"),            # Plus operator
        ("ID", r"[A-Za-z]+"),       # Identifiers (variable names)
        ("SKIP", r"[ \t\n]"),       # Skip spaces and tabs
        ("MISMATCH", r"."),         # Error for unexpected characters
    ]
    
    master_pattern = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    regex = re.compile(master_pattern)
    
    tokens = []
    for match in regex.finditer(input_str):
        kind = match.lastgroup
        value = match.group()
        
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise ValueError(f"Unexpected character {value} at position {match.start()}")
        else:
            tokens.append((kind, value))
    
    return tokens