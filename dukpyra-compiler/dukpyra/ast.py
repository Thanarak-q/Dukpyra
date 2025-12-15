"""
Dukpyra AST - Abstract Syntax Tree Node Definitions

This module defines all AST nodes used by the Dukpyra compiler.
The parser creates these nodes, and the code generator traverses them
to produce C# code.

Architecture:
    Source Code → Lexer → Parser → AST → CodeGen → C# Code
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Any


# ==============================================================================
# Base Node
# ==============================================================================

@dataclass
class Node:
    """Base class for all AST nodes"""
    lineno: int = 0  # Line number in source file for error reporting


# ==============================================================================
# Program Structure
# ==============================================================================

@dataclass
class ProgramNode(Node):
    """
    Root node representing an entire Dukpyra program.
    
    Contains:
    - imports: List of import statements
    - app_creation: The app = dukpyra.app() statement (optional)
    - classes: List of class definitions (for request/response bodies)
    - endpoints: List of API endpoint definitions
    """
    imports: List['ImportNode'] = field(default_factory=list)
    app_creation: Optional['AppCreationNode'] = None
    classes: List['ClassDefNode'] = field(default_factory=list)
    endpoints: List['EndpointNode'] = field(default_factory=list)


@dataclass
class ImportNode(Node):
    """
    Represents: import dukpyra
    
    Note: In C# output, imports are handled by .NET's implicit usings,
    so this is mainly for syntax compatibility with Python.
    """
    module_name: str = ""


@dataclass
class AppCreationNode(Node):
    """
    Represents: app = dukpyra.app()
    
    Attributes:
        var_name: The variable name (e.g., "app")
        module_name: The module being called (e.g., "dukpyra") 
        func_name: The function being called (e.g., "app")
    """
    var_name: str = ""
    module_name: str = ""
    func_name: str = ""


# ==============================================================================
# Class Definitions (for Request Bodies)
# ==============================================================================

@dataclass
class ClassDefNode(Node):
    """
    Represents a class definition for request/response bodies.
    
    Example:
        class CreateUserRequest:
            name: str
            email: str
            age: int
    
    Attributes:
        name: The class name
        properties: List of typed properties
    """
    name: str = ""
    properties: List['ClassPropertyNode'] = field(default_factory=list)


@dataclass
class ClassPropertyNode(Node):
    """
    Represents a typed property in a class.
    
    Example: name: str
    
    Attributes:
        name: Property name
        type_hint: The type annotation (str, int, etc.)
    """
    name: str = ""
    type_hint: str = ""


# ==============================================================================
# Endpoint Definition
# ==============================================================================

@dataclass
class EndpointNode(Node):
    """
    Represents a complete API endpoint (decorator + function).
    
    Example:
        @app.get("/users")
        def get_users():
            return {"users": []}
    """
    decorator: 'DecoratorNode' = None
    function: 'FunctionDefNode' = None
    raw_csharp: Optional[str] = None


@dataclass  
class DecoratorNode(Node):
    """
    Represents: @app.get("/path") or @app.post("/path") etc.
    
    Attributes:
        app_name: The app variable name (e.g., "app")
        method: HTTP method (e.g., "get", "post", "put", "delete", "patch")
        path: URL path (e.g., "/users", "/health")
    """
    app_name: str = ""
    method: str = ""  # get, post, put, delete, patch
    path: str = ""


@dataclass
class FunctionDefNode(Node):
    """
    Represents a function definition.
    
    Example:
        def get_users():
            return {"users": []}
    
    Attributes:
        name: Function name
        params: List of parameters (for future use)
        body: The return expression
    """
    name: str = ""
    params: List['ParameterNode'] = field(default_factory=list)
    body: 'ExpressionNode' = None


@dataclass
class ParameterNode(Node):
    """
    Represents a function parameter.
    
    Example: user_id: int = 0
    
    Note: Currently not used, but prepared for path/query parameter support.
    """
    name: str = ""
    type_hint: Optional[str] = None
    default_value: Optional['ExpressionNode'] = None


# ==============================================================================
# Expressions
# ==============================================================================

@dataclass
class ExpressionNode(Node):
    """Base class for all expression nodes"""
    pass


@dataclass
class StringExpr(ExpressionNode):
    """
    String literal: "hello" or 'hello'
    
    The value stored has quotes already stripped by the lexer.
    """
    value: str = ""


@dataclass
class NumberExpr(ExpressionNode):
    """
    Number literal: 42 or 3.14
    
    Stores as Python int or float, codegen converts to string.
    """
    value: Union[int, float] = 0


@dataclass
class BoolExpr(ExpressionNode):
    """
    Boolean literal: True or False
    
    Converts to C#: true or false
    """
    value: bool = False


@dataclass
class NoneExpr(ExpressionNode):
    """
    None literal: None
    
    Converts to C#: null
    """
    pass


@dataclass
class IdentifierExpr(ExpressionNode):
    """
    Variable reference: user_id, name, etc.
    
    Note: For future use when we support variables in return statements.
    """
    name: str = ""


@dataclass
class MemberAccessExpr(ExpressionNode):
    """
    Member access expression: body.name, user.email, etc.
    
    Example:
        body.name → object.member
    
    Converts to C#: body.name (same syntax)
    """
    object_name: str = ""
    member_name: str = ""


@dataclass
class DictExpr(ExpressionNode):
    """
    Dictionary literal: {"key": "value", "count": 42}
    
    Converts to C# anonymous object: new { key = "value", count = 42 }
    """
    items: List['DictItemNode'] = field(default_factory=list)


@dataclass
class DictItemNode(Node):
    """
    A single key-value pair in a dictionary.
    
    Example: "name": "John"
    """
    key: str = ""  # Always a string (dictionary key)
    value: ExpressionNode = None


@dataclass
class ListExpr(ExpressionNode):
    """
    List literal: [1, 2, 3] or ["a", "b", "c"]
    
    Note: For future use.
    Converts to C#: new[] { 1, 2, 3 }
    """
    items: List[ExpressionNode] = field(default_factory=list)


# ==============================================================================
# Helper Functions
# ==============================================================================

def ast_to_dict(node: Node) -> dict:
    """
    Convert an AST node to a dictionary for debugging/testing.
    
    Usage:
        ast = parser.parse(code)
        print(ast_to_dict(ast))
    """
    if node is None:
        return None
    
    if isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    
    if not isinstance(node, Node):
        return node
    
    result = {"_type": type(node).__name__}
    
    for field_name, field_value in node.__dict__.items():
        if field_name.startswith("_"):
            continue
        if isinstance(field_value, Node):
            result[field_name] = ast_to_dict(field_value)
        elif isinstance(field_value, list):
            result[field_name] = [ast_to_dict(item) for item in field_value]
        else:
            result[field_name] = field_value
    
    return result


def print_ast(node: Node, indent: int = 0) -> None:
    """
    Pretty print an AST for debugging.
    
    Usage:
        ast = parser.parse(code)
        print_ast(ast)
    """
    import json
    print(json.dumps(ast_to_dict(node), indent=2, ensure_ascii=False))
