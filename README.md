# Lexical Analyzer Project

A FastAPI-based lexical analyzer that tokenizes Python code strings. This project solves Question 1 by implementing a complete lexical analysis system with tokenization, whitespace removal, and error handling.

## Problem Statement (Question 1)

For the Python statement `x = 10 + 5`:
- Write a function that takes the string as input
- Remove all whitespace characters from the input string
- Tokenize the cleaned string using Python's `re` (regular expression) module
- Return a list of tuples where each tuple represents a token and its type
- Implement error handling for unexpected characters with their positions

## Solution Overview

The project solves this problem through a modular architecture:

### 1. **Whitespace Removal** (`app/services/string_operations.py`)
- Function: `remove_whitespace(input_str: str) -> str`
- Removes ALL whitespace characters (spaces, tabs, newlines) using regex
- Example: `"x = 10 + 5"` → `"x=10+5"`

### 2. **Tokenization** (`app/utils/tokenizer.py`)
- Function: `tokenize_string(input_str: str)`
- Uses ordered regex patterns to identify and classify tokens:
  - **Numbers**: `NUMBER` (integers), `DECIMAL` (floats e.g., `3.14`)
  - **Identifiers**: `ID` (variable names with underscores and digits, e.g., `my_var`, `var1`)
  - **Arithmetic Operators**: `ASSIGN` (`=`), `PLUS` (`+`), `MINUS` (`-`), `MULT` (`*`), `DIV` (`/`), `MOD` (`%`), `FLOORDIV` (`//`)
  - **Comparison Operators**: `EQ` (`==`), `NEQ` (`!=`), `LT` (`<`), `GT` (`>`), `LEQ` (`<=`), `GEQ` (`>=`)
  - **Brackets**: `LPAREN` (`(`), `RPAREN` (`)`), `LBRACKET` (`[`), `RBRACKET` (`]`), `LBRACE` (`{`), `RBRACE` (`}`)
  - **Others**: `COMMA` (`,`)
  - **Invalid**: `MISMATCH` (unexpected characters)
- Returns a list of tuples `(token_type, token_value)`
- Example output: `[('ID', 'x'), ('ASSIGN', '='), ('NUMBER', '10'), ('PLUS', '+'), ('NUMBER', '5')]`
- Pattern ordering ensures proper precedence (e.g., `//` matches before `/`)

### 3. **Error Handling**
- **Invalid Characters**: When an unexpected character is encountered (e.g., `@`, `#`, etc.), the tokenizer raises a `ValueError` with the character and its position
- **API Response**: Errors are caught and returned as JSON with an `error` field
- **Example**: Input `"x = 10 @ 5"` returns `{"error": "Unexpected character @ at position 7"}`

### 4. **FastAPI Endpoint** (`app/api/endpoints.py`)
- Endpoint: `POST /process_string/`
- Request body: `{"input_str": "your input string"}`
- Response: `{"tokens": [(...), (...), ...]}`  or `{"error": "error message"}`

## Project Structure

```
server/
├── main.py                          # FastAPI application entry point
├── pyproject.toml                   # Project dependencies
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── endpoints.py             # API route definitions
│   ├── services/
│   │   └── string_operations.py     # Whitespace removal logic
│   └── utils/
│       └── tokenizer.py             # Tokenization logic
└── tests/
    └── test_main.py                 # Unit tests for happy and sad paths
```

## Installation

### Prerequisites
- Python 3.13+
- `uv` package manager (install via `pip install uv`)

### Setup Steps

1. **Clone/Navigate to the project**
   ```bash
   cd server
   ```

2. **Install project dependencies using `uv`**
   ```bash
   uv sync
   ```
   This command will:
   - Create/update the virtual environment
   - Install all dependencies from `pyproject.toml`
   - Install development dependencies

3. **Activate the virtual environment** (if needed)
   ```bash
   source .venv/Scripts/activate  # On Windows
   # or
   source .venv/bin/activate      # On macOS/Linux
   ```

## Running the Project

### Option 1: Run Locally

#### Start the API Server

```bash
uv run uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### Option 2: Run with Docker Compose

#### Prerequisites
- Docker and Docker Compose installed

#### Start the Application

```bash
docker-compose up
```

The server will start at `http://127.0.0.1:8000`

#### Stop the Application

```bash
docker-compose down
```

#### Rebuild the Docker Image

```bash
docker-compose up --build
```

### Option 3: Run with Docker Standalone

```bash
docker build -t lexical-analyzer .
docker run -p 8000:8000 lexical-analyzer
```

### API Documentation

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs`
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc`

### Example API Call

**Happy Path** (valid input):
```bash
curl -X POST "http://127.0.0.1:8000/process_string/" \
  -H "Content-Type: application/json" \
  -d '{"input_str": "x = 10 + 5"}'
```

**Response**:
```json
{
  "tokens": [
    ["ID", "x"],
    ["ASSIGN", "="],
    ["NUMBER", "10"],
    ["PLUS", "+"],
    ["NUMBER", "5"]
  ]
}
```

**Sad Path** (invalid character):
```bash
curl -X POST "http://127.0.0.1:8000/process_string/" \
  -H "Content-Type: application/json" \
  -d '{"input_str": "x = 10 @ 5"}'
```

**Response**:
```json
{
  "error": "Unexpected character @ at position 7"
}
```

## Running Tests

### Execute All Tests

```bash
uv run pytest
```

### Run Tests with Verbose Output

```bash
uv run pytest -v
```

### Test Coverage

The test suite includes **34 comprehensive tests**:

#### **Happy Path Tests (21 tests)** ✅
Tests for all supported features:
- **Arithmetic Operators**: Addition, subtraction, multiplication, division, floor division, modulo
- **Comparison Operators**: Equality, inequality, less than, greater than, less-equal, greater-equal
- **Variable Names**: Standard names, underscores (`my_var`), digits in names (`var1`)
- **Number Types**: Integers, decimal numbers (e.g., `3.14`)
- **Brackets & Symbols**: Parentheses, square brackets, curly braces, commas
- **Complex Expressions**: Multiple operators and nested parentheses
- **Whitespace Handling**: Various whitespace types (spaces, tabs, multiple spaces)

Example test cases:
- `"x = 10 + 5"` → Tokens successfully extracted
- `"my_var = 3.14"` → Decimal and underscore support
- `"result = (a + b) * c"` → Complex expressions
- `"x <= 10"` → Comparison operators

#### **Sad Path Tests (13 tests)** ❌
Tests for error handling:
- Invalid characters: `@`, `#`, `&`, `|`, `^`, `~`, `;`, `:`, `\`, `'`
- Unicode/accented characters: `café`
- Error message validation: Ensures character and position are reported

All error cases properly return `{"error": "Unexpected character <char> at position <pos>"}`

### Expected Test Output

```
================================== test session starts ==================================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
collected 34 items

tests/test_main.py ..................................                                [100%]

=================================== 34 passed in 0.57s ===================================
```

## Supported Token Types and Error Handling

### Supported Tokens

| Token Type | Symbols | Examples |
|-----------|---------|----------|
| **Numbers** | `NUMBER`, `DECIMAL` | `10`, `3.14`, `0`, `99` |
| **Identifiers** | `ID` | `x`, `my_var`, `var1`, `_private` |
| **Arithmetic** | `PLUS`, `MINUS`, `MULT`, `DIV`, `FLOORDIV`, `MOD` | `+`, `-`, `*`, `/`, `//`, `%` |
| **Assignment** | `ASSIGN` | `=` |
| **Comparison** | `EQ`, `NEQ`, `LT`, `GT`, `LEQ`, `GEQ` | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Brackets** | `LPAREN`, `RPAREN`, `LBRACKET`, `RBRACKET`, `LBRACE`, `RBRACE` | `(`, `)`, `[`, `]`, `{`, `}` |
| **Other** | `COMMA` | `,` |

### Error Handling Strategy

| Scenario | Input | Behavior | Response |
|----------|-------|----------|----------|
| **Valid arithmetic** | `"x = 20 - 3"` | Successful tokenization | `{"tokens": [...]}` |
| **Decimal numbers** | `"pi = 3.14"` | DECIMAL token recognized | `{"tokens": [...]}` |
| **Variables with underscore** | `"my_var = 10"` | ID token includes underscore | `{"tokens": [...]}` |
| **Variables with digits** | `"var1 = 5"` | ID token includes digits | `{"tokens": [...]}` |
| **Comparison operators** | `"x <= 10"` | Multiple operators supported | `{"tokens": [...]}` |
| **Complex expressions** | `"(a + b) * c"` | Nested brackets supported | `{"tokens": [...]}` |
| **Invalid character @** | `"x @ 5"` | MISMATCH token raised | `{"error": "Unexpected character @ at position 3"}` |
| **Invalid character #** | `"x = 10 # comment"` | Comments not supported | `{"error": "Unexpected character # at position 8"}` |
| **Unicode character** | `"café = 10"` | Non-ASCII not supported | `{"error": "Unexpected character é at position 3"}` |
| **Empty string** | `""` | Returns empty token list | `{"tokens": []}` |

## Key Technologies

- **FastAPI**: Modern async web framework
- **Pydantic**: Request/response validation
- **Python Regex (`re`)**: Pattern matching for tokenization
- **pytest**: Unit testing framework
- **uvicorn**: ASGI server

## Notes

- **Whitespace Handling**: Uses regex `\s+` to remove ALL whitespace types (spaces, tabs, newlines), not just spaces
- **Pattern Ordering**: Longer patterns are matched first to prevent partial matches (e.g., `//` before `/`, `==` before `=`)
- **Variable Names**: Support Python conventions with underscores and digits (e.g., `_private`, `var1`, `my_var`)
- **Decimal Support**: Recognizes floating-point numbers (e.g., `3.14`, `10.5`)
- **Comprehensive Operators**: Supports all basic arithmetic, comparison, and logical operators
- **Error Messages**: Include exact character and position for easy debugging
- **Extensible Design**: Easy to add more token types by adding patterns to the token specification
- **JSON API**: All endpoints return JSON for seamless frontend integration
- **Well-Tested**: 34 comprehensive tests covering both happy and sad paths

## Recent Improvements (v2.0)

✅ Fixed whitespace removal to handle tabs, newlines, and multiple spaces  
✅ Added support for 10+ new operators (-, *, /, //, %, ==, !=, <, >, <=, >=)  
✅ Added decimal number support (3.14, 0.5, etc.)  
✅ Improved variable naming to support underscores and digits  
✅ Added support for brackets, parentheses, braces, and commas  
✅ Expanded test suite from 2 to 34 comprehensive tests  
✅ Better error messages with character position information

## Author

Developed as a solution for Semester 07 TPL - Lexical Analyzer Assignment
