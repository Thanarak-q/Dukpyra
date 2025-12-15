"""
Dukpyra Compiler Unit Tests - Lexer

Comprehensive tests for the lexer module that tokenizes Python source code.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dukpyra.lexer import lexer


class TestLexerKeywords:
    """Test reserved keywords are tokenized correctly."""
    
    def test_import_keyword(self):
        lexer.input("import")
        tok = lexer.token()
        assert tok.type == "IMPORT"
        assert tok.value == "import"
    
    def test_def_keyword(self):
        lexer.input("def")
        tok = lexer.token()
        assert tok.type == "DEF"
    
    def test_class_keyword(self):
        lexer.input("class")
        tok = lexer.token()
        assert tok.type == "CLASS"
    
    def test_return_keyword(self):
        lexer.input("return")
        tok = lexer.token()
        assert tok.type == "RETURN"
    
    def test_http_methods(self):
        for method in ["get", "post", "put", "delete", "patch"]:
            lexer.input(method)
            tok = lexer.token()
            assert tok.type == method.upper()


class TestLexerLiterals:
    """Test literal values are tokenized correctly."""
    
    def test_true_literal(self):
        lexer.input("True")
        tok = lexer.token()
        assert tok.type == "TRUE"
    
    def test_false_literal(self):
        lexer.input("False")
        tok = lexer.token()
        assert tok.type == "FALSE"
    
    def test_none_literal(self):
        lexer.input("None")
        tok = lexer.token()
        assert tok.type == "NONE"
    
    def test_integer(self):
        lexer.input("42")
        tok = lexer.token()
        assert tok.type == "NUMBER"
        assert tok.value == 42
    
    def test_float(self):
        lexer.input("3.14")
        tok = lexer.token()
        assert tok.type == "NUMBER"
        assert tok.value == 3.14
    
    def test_double_quoted_string(self):
        lexer.input('"hello"')
        tok = lexer.token()
        assert tok.type == "STRING"
        assert tok.value == "hello"
    
    def test_single_quoted_string(self):
        lexer.input("'world'")
        tok = lexer.token()
        assert tok.type == "STRING"
        assert tok.value == "world"


class TestLexerSymbols:
    """Test symbols are tokenized correctly."""
    
    def test_parentheses(self):
        lexer.input("()")
        t1 = lexer.token()
        t2 = lexer.token()
        assert t1.type == "LPAREN"
        assert t2.type == "RPAREN"
    
    def test_braces(self):
        lexer.input("{}")
        t1 = lexer.token()
        t2 = lexer.token()
        assert t1.type == "LBRACE"
        assert t2.type == "RBRACE"
    
    def test_brackets(self):
        lexer.input("[]")
        t1 = lexer.token()
        t2 = lexer.token()
        assert t1.type == "LBRACKET"
        assert t2.type == "RBRACKET"
    
    def test_at_symbol(self):
        lexer.input("@")
        tok = lexer.token()
        assert tok.type == "AT"
    
    def test_dot(self):
        lexer.input(".")
        tok = lexer.token()
        assert tok.type == "DOT"


class TestLexerTypeHints:
    """Test type hint keywords."""
    
    def test_type_int(self):
        lexer.input("int")
        tok = lexer.token()
        assert tok.type == "TYPE_INT"
    
    def test_type_str(self):
        lexer.input("str")
        tok = lexer.token()
        assert tok.type == "TYPE_STR"
    
    def test_type_float(self):
        lexer.input("float")
        tok = lexer.token()
        assert tok.type == "TYPE_FLOAT"
    
    def test_type_bool(self):
        lexer.input("bool")
        tok = lexer.token()
        assert tok.type == "TYPE_BOOL"


class TestLexerDecorator:
    """Test complete decorator tokenization."""
    
    def test_decorator(self):
        lexer.input('@app.get("/users")')
        tokens = []
        while True:
            tok = lexer.token()
            if tok is None:
                break
            tokens.append(tok.type)
        assert tokens == ["AT", "ID", "DOT", "GET", "LPAREN", "STRING", "RPAREN"]


class TestLexerFunctionDef:
    """Test function definition tokenization."""
    
    def test_function_def(self):
        lexer.input("def hello():")
        tokens = []
        while True:
            tok = lexer.token()
            if tok is None:
                break
            tokens.append(tok.type)
        assert tokens == ["DEF", "ID", "LPAREN", "RPAREN", "COLON"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
