# tests/test_main.py
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app  # Import the FastAPI app from main.py

client = TestClient(app)

# ============= HAPPY PATH TESTS =============

def test_simple_assignment_with_addition():
    """Test basic assignment with addition"""
    response = client.post("/process_string/", json={"input_str": "x = 10 + 5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    assert len(result["tokens"]) == 5

def test_subtraction():
    """Test subtraction operator"""
    response = client.post("/process_string/", json={"input_str": "a = 20 - 3"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["MINUS", "-"] in tokens

def test_multiplication():
    """Test multiplication operator"""
    response = client.post("/process_string/", json={"input_str": "b = 4 * 5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["MULT", "*"] in tokens

def test_division():
    """Test division operator"""
    response = client.post("/process_string/", json={"input_str": "c = 10 / 2"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["DIV", "/"] in tokens

def test_floor_division():
    """Test floor division operator"""
    response = client.post("/process_string/", json={"input_str": "d = 10 // 3"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["FLOORDIV", "//"] in tokens

def test_modulo():
    """Test modulo operator"""
    response = client.post("/process_string/", json={"input_str": "e = 10 % 3"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["MOD", "%"] in tokens

def test_variable_with_underscore():
    """Test variable names with underscores"""
    response = client.post("/process_string/", json={"input_str": "my_var = 10"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["ID", "my_var"] in tokens

def test_variable_with_digits():
    """Test variable names with digits"""
    response = client.post("/process_string/", json={"input_str": "var1 = 5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["ID", "var1"] in tokens

def test_decimal_numbers():
    """Test decimal number support"""
    response = client.post("/process_string/", json={"input_str": "pi = 3.14"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["DECIMAL", "3.14"] in tokens

def test_comparison_equal():
    """Test equality operator"""
    response = client.post("/process_string/", json={"input_str": "x == 5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["EQ", "=="] in tokens

def test_less_than_equal():
    """Test less than or equal operator"""
    response = client.post("/process_string/", json={"input_str": "x <= 10"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["LEQ", "<="] in tokens

def test_greater_than_equal():
    """Test greater than or equal operator"""
    response = client.post("/process_string/", json={"input_str": "x >= 5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["GEQ", ">="] in tokens

def test_not_equal():
    """Test not equal operator"""
    response = client.post("/process_string/", json={"input_str": "x != 0"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["NEQ", "!="] in tokens

def test_less_than():
    """Test less than operator"""
    response = client.post("/process_string/", json={"input_str": "x < 100"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["LT", "<"] in tokens

def test_greater_than():
    """Test greater than operator"""
    response = client.post("/process_string/", json={"input_str": "x > 0"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["GT", ">"] in tokens

def test_parentheses():
    """Test parentheses"""
    response = client.post("/process_string/", json={"input_str": "(x + 5)"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["LPAREN", "("] in tokens
    assert ["RPAREN", ")"] in tokens

def test_brackets():
    """Test square brackets"""
    response = client.post("/process_string/", json={"input_str": "arr[0]"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["LBRACKET", "["] in tokens
    assert ["RBRACKET", "]"] in tokens

def test_braces():
    """Test curly braces"""
    response = client.post("/process_string/", json={"input_str": "dict{key}"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["LBRACE", "{"] in tokens
    assert ["RBRACE", "}"] in tokens

def test_comma():
    """Test comma support"""
    response = client.post("/process_string/", json={"input_str": "x, y"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["COMMA", ","] in tokens

def test_negative_number():
    """Test negative number"""
    response = client.post("/process_string/", json={"input_str": "x = -5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    tokens = result["tokens"]
    assert ["MINUS", "-"] in tokens
    assert ["NUMBER", "5"] in tokens

def test_complex_expression():
    """Test complex expression with multiple operators"""
    response = client.post("/process_string/", json={"input_str": "result = (a + b) * c"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result
    assert len(result["tokens"]) > 0

def test_whitespace_variations():
    """Test various whitespace characters are handled"""
    response = client.post("/process_string/", json={"input_str": "x  =  10  +  5"})
    assert response.status_code == 200
    result = response.json()
    assert "tokens" in result

# ============= SAD PATH TESTS =============

def test_invalid_character_at_sign():
    """Test error handling for @ symbol"""
    response = client.post("/process_string/", json={"input_str": "x = 10 @ 5"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "@" in result["error"]

def test_invalid_character_hash():
    """Test error handling for # symbol (comment not supported)"""
    response = client.post("/process_string/", json={"input_str": "x = 10 # comment"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "#" in result["error"]

def test_invalid_character_ampersand():
    """Test error handling for & symbol"""
    response = client.post("/process_string/", json={"input_str": "x & y"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "&" in result["error"]

def test_invalid_character_pipe():
    """Test error handling for | symbol"""
    response = client.post("/process_string/", json={"input_str": "x | y"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "|" in result["error"]

def test_invalid_character_caret():
    """Test error handling for ^ symbol"""
    response = client.post("/process_string/", json={"input_str": "x ^ y"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "^" in result["error"]

def test_invalid_character_tilde():
    """Test error handling for ~ symbol"""
    response = client.post("/process_string/", json={"input_str": "~x"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "~" in result["error"]

def test_invalid_character_semicolon():
    """Test error handling for ; symbol"""
    response = client.post("/process_string/", json={"input_str": "x = 5;"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert ";" in result["error"]

def test_invalid_character_colon():
    """Test error handling for : symbol"""
    response = client.post("/process_string/", json={"input_str": "x : int"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert ":" in result["error"]

def test_invalid_character_backslash():
    """Test error handling for backslash symbol"""
    response = client.post("/process_string/", json={"input_str": "x \\ y"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result

def test_invalid_character_quote():
    """Test error handling for quote symbol"""
    response = client.post("/process_string/", json={"input_str": "x = 'hello'"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result

def test_unicode_character():
    """Test error handling for unicode/accented characters"""
    response = client.post("/process_string/", json={"input_str": "café = 10"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result

def test_error_message_includes_position():
    """Test that error message includes character position"""
    response = client.post("/process_string/", json={"input_str": "x @ 5"})
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert "position" in result["error"].lower()