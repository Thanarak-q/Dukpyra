"""
Dukpyra - Python to ASP.NET Core Compiler

A transpiler that converts Python web API definitions to C# ASP.NET Core Minimal API.

Architecture:
    Source Code → Lexer → Parser → AST → Analyzer → CodeGen → C# Code

Modules:
    - lexer: Tokenizes Python source code
    - parser: Builds AST from token stream
    - ast: AST node definitions
    - analyzer: Semantic analysis and validation
    - codegen: Generates C# code from AST
    - cli: Command-line interface
    - runtime: Runtime shim for profiling
"""

__version__ = "0.3.0"
__author__ = "Rock"

from .lexer import lexer
from .parser import parse
from .ast import ProgramNode, EndpointNode, FunctionDefNode, ClassDefNode
from .analyzer import analyze, SemanticAnalyzer, SemanticError, SemanticWarning
from .codegen import generate_csharp, CSharpCodeGenerator
# Export runtime components for user code
from .runtime import app, raw_csharp, _runtime

__all__ = [
    # Version
    '__version__',
    
    # Runtime (For User Code)
    'app',
    'raw_csharp',
    '_runtime',
    
    # Lexer
    'lexer',
    
    # Parser
    'parse',
    
    # AST
    'ProgramNode',
    'EndpointNode', 
    'FunctionDefNode',
    'ClassDefNode',
    
    # Analyzer
    'analyze',
    'SemanticAnalyzer',
    'SemanticError',
    'SemanticWarning',
    
    # Code Generation
    'generate_csharp',
    'CSharpCodeGenerator',
]
