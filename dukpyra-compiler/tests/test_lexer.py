import pytest
from dukpyra.lexer import lexer

def test_lexer_basic():
    """Test basic tokenization"""
    code = '@app.get("/")'
    lexer.input(code)

    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok.type)

    assert 'AT' in tokens
    assert 'APP' in tokens
    assert 'DOT' in tokens
    assert 'GET' in tokens
    assert 'STRING' in tokens

def test_lexer_function():
    """Test function tokenization"""
    code = 'def home():'
    lexer.input(code)

    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok.type)

    assert 'DEF' in tokens
    assert 'ID' in tokens
    assert 'LPAREN' in tokens
    assert 'RPAREN' in tokens
    assert 'COLON' in tokens
