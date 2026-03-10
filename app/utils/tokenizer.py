# app/utils/tokenizer.py
import re

def tokenize_string(input_str: str):
    """Tokenizes the string using regular expressions."""
    
    # Order matters: longer patterns first to avoid partial matches
    token_specification = [
        ("FLOORDIV", r"//"),        # Floor division operator
        ("LEQ", r"<="),             # Less than or equal
        ("GEQ", r">="),             # Greater than or equal
        ("EQ", r"=="),              # Equality operator
        ("NEQ", r"!="),             # Not equal operator
        ("DECIMAL", r"\d+\.\d+"),   # Decimal numbers
        ("NUMBER", r"\d+"),         # Integer
        ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),  # Identifiers (with underscores and digits)
        ("ASSIGN", r"="),           # Assignment operator
        ("PLUS", r"\+"),            # Plus operator
        ("MINUS", r"-"),            # Minus operator
        ("MULT", r"\*"),            # Multiplication operator
        ("DIV", r"/"),              # Division operator
        ("MOD", r"%"),              # Modulo operator
        ("LT", r"<"),               # Less than
        ("GT", r">"),               # Greater than
        ("LPAREN", r"\("),          # Left parenthesis
        ("RPAREN", r"\)"),          # Right parenthesis
        ("LBRACKET", r"\["),        # Left bracket
        ("RBRACKET", r"\]"),        # Right bracket
        ("LBRACE", r"\{"),          # Left brace
        ("RBRACE", r"\}"),          # Right brace
        ("COMMA", r","),            # Comma
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