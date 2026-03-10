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
- Removes all space characters from the input string
- Example: `"x = 10 + 5"` → `"x=10+5"`

### 2. **Tokenization** (`app/utils/tokenizer.py`)
- Function: `tokenize_string(input_str: str)`
- Uses regex patterns to identify and classify tokens:
  - `NUMBER`: Integer values (e.g., `10`, `5`)
  - `ID`: Identifiers/variable names (e.g., `x`)
  - `ASSIGN`: Assignment operator (`=`)
  - `PLUS`: Addition operator (`+`)
  - `MISMATCH`: Unexpected/invalid characters
- Returns a list of tuples `(token_type, token_value)`
- Example output: `[('ID', 'x'), ('ASSIGN', '='), ('NUMBER', '10'), ('PLUS', '+'), ('NUMBER', '5')]`

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

The test suite includes:

#### **Happy Path Test** (`test_process_string`)
- Input: `"x = 10 + 5"`
- Expected: Status code 200 with `tokens` in response
- Validates: Successful tokenization of valid Python code

#### **Sad Path Test** (`test_invalid_character`)
- Input: `"x = 10 @ 5"` (contains invalid `@` symbol)
- Expected: Status code 200 with `error` in response
- Validates: Proper error handling for unexpected characters

### Expected Test Output

```
================================== test session starts ==================================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
collected 2 items

tests/test_main.py ..                                                               [100%]

=================================== 2 passed in 0.36s ===================================
```

## Error Handling Strategy

| Scenario | Input | Behavior | Response |
|----------|-------|----------|----------|
| Valid input | `"x = 10 + 5"` | Successful tokenization | Returns token list |
| Unknown operator | `"a @ b"` | Catches MISMATCH token | Returns error with position |
| Special characters | `"x & y"` | Catches MISMATCH token | Returns error with position |
| Empty string | `""` | Returns empty token list | `{"tokens": []}` |

## Key Technologies

- **FastAPI**: Modern async web framework
- **Pydantic**: Request/response validation
- **Python Regex (`re`)**: Pattern matching for tokenization
- **pytest**: Unit testing framework
- **uvicorn**: ASGI server

## Notes

- The tokenizer uses a master regex pattern combining all token specifications
- Whitespace is automatically skipped during tokenization
- Error messages include the exact character and its position for debugging
- All endpoints return JSON for easy integration with frontend applications

## Author

Developed as a solution for Semester 07 TPL - Lexical Analyzer Assignment
