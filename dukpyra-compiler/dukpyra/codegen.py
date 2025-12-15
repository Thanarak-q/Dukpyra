"""
Dukpyra Code Generator - AST to C# Transpiler

This module walks the AST and generates C# code for ASP.NET Core Minimal API.

Architecture:
    Source Code → Lexer → Parser → AST → CodeGen → C# Code
                                          ^^^^^^^
                                          This module
"""

from typing import List
from .ast import (
    Node,
    ProgramNode,
    ImportNode,
    AppCreationNode,
    ClassDefNode,
    ClassPropertyNode,
    EndpointNode,
    DecoratorNode,
    FunctionDefNode,
    ParameterNode,
    ExpressionNode,
    StringExpr,
    NumberExpr,
    BoolExpr,
    NoneExpr,
    IdentifierExpr,
    MemberAccessExpr,
    DictExpr,
    DictItemNode,
    ListExpr,
)


class CSharpCodeGenerator:
    """
    Generates C# ASP.NET Core Minimal API code from Dukpyra AST.
    
    Uses the Visitor pattern to traverse the AST.
    
    Usage:
        ast = parser.parse(source_code)
        generator = CSharpCodeGenerator()
        csharp_code = generator.generate(ast)
    """
    
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces
    
    def generate(self, program: ProgramNode) -> str:
        """
        Generate complete C# code from a ProgramNode.
        
        Returns a complete Program.cs file content.
        """
        if program is None:
            return ""
        
        lines = []
        
        # Generate C# record types from class definitions
        for class_def in program.classes:
            lines.append(self.visit_class(class_def))
        
        if program.classes:
            lines.append("")  # Blank line after records
        
        # Header
        lines.extend([
            "var builder = WebApplication.CreateBuilder(args);",
            "var app = builder.Build();",
            "",
            "// --- Dukpyra Generated Routes ---",
        ])
        
        # Generate each endpoint
        for endpoint in program.endpoints:
            lines.append(self.visit_endpoint(endpoint))
        
        # Footer
        lines.extend([
            "// --------------------------------",
            "",
            "app.Run();",
        ])
        
        return "\n".join(lines)
    
    def visit_class(self, node: ClassDefNode) -> str:
        """
        Generate C# record type from class definition.
        
        Input (Python):
            class CreateUser:
                name: str
                email: str
        
        Output (C#):
            public record CreateUser(string name, string email);
        """
        params = []
        for prop in node.properties:
            csharp_type = self.python_type_to_csharp(prop.type_hint)
            params.append(f"{csharp_type} {prop.name}")
        
        params_str = ", ".join(params)
        return f"public record {node.name}({params_str});"
    
    def visit_endpoint(self, node: EndpointNode) -> str:
        """
        Generate C# code for an endpoint.
        
        Input (Python):
            @app.get("/users/{id}")
            def get_user(id: int):
                return {"user_id": id}
        
        Output (C#):
            app.MapGet("/users/{id}", (int id) =>
            {
                return Results.Ok(new { user_id = id });
            });
        """
        method = node.decorator.method.capitalize()  # get -> Get
        path = node.decorator.path
        params = self.visit_params(node.function.params)
        body = self.visit_function_body(node.function)
        
        return f'''
app.Map{method}("{path}", ({params}) =>
{{
    {body}
}});'''
    
    def visit_params(self, params: list) -> str:
        """
        Generate C# lambda parameter list.
        
        Input (Python): [ParameterNode(name="id", type_hint="int")]
        Output (C#):    "int id"
        """
        if not params:
            return ""
        
        param_strs = []
        for param in params:
            csharp_type = self.python_type_to_csharp(param.type_hint)
            param_strs.append(f"{csharp_type} {param.name}")
        
        return ", ".join(param_strs)
    
    def python_type_to_csharp(self, python_type: str) -> str:
        """
        Convert Python type hint to C# type.
        
        Python -> C#:
            int    -> int
            str    -> string
            float  -> double
            bool   -> bool
            None   -> dynamic (for untyped parameters)
        """
        type_map = {
            "int": "int",
            "str": "string",
            "float": "double",
            "bool": "bool",
        }
        
        if python_type is None:
            return "dynamic"  # Untyped parameter
        
        return type_map.get(python_type, python_type)
    
    def visit_function_body(self, node: FunctionDefNode) -> str:
        """
        Generate C# code for function body.
        
        Currently only supports return statements.
        """
        if node.body is None:
            return "return Results.Ok();"
        
        expr = self.visit_expression(node.body)
        return f"return Results.Ok({expr});"
    
    def visit_expression(self, node: ExpressionNode) -> str:
        """
        Dispatch to the appropriate expression visitor.
        """
        if isinstance(node, StringExpr):
            return self.visit_string(node)
        elif isinstance(node, NumberExpr):
            return self.visit_number(node)
        elif isinstance(node, BoolExpr):
            return self.visit_bool(node)
        elif isinstance(node, NoneExpr):
            return self.visit_none(node)
        elif isinstance(node, IdentifierExpr):
            return self.visit_identifier(node)
        elif isinstance(node, MemberAccessExpr):
            return self.visit_member_access(node)
        elif isinstance(node, DictExpr):
            return self.visit_dict(node)
        elif isinstance(node, ListExpr):
            return self.visit_list(node)
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")
    
    def visit_string(self, node: StringExpr) -> str:
        """
        Convert Python string to C# string.
        
        Python: "hello"
        C#:     "hello"
        """
        # Escape special characters for C#
        escaped = node.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    
    def visit_number(self, node: NumberExpr) -> str:
        """
        Convert Python number to C# number.
        
        Python: 42 or 3.14
        C#:     42 or 3.14
        """
        return str(node.value)
    
    def visit_bool(self, node: BoolExpr) -> str:
        """
        Convert Python bool to C# bool.
        
        Python: True / False
        C#:     true / false
        """
        return "true" if node.value else "false"
    
    def visit_none(self, node: NoneExpr) -> str:
        """
        Convert Python None to C# null.
        
        Python: None
        C#:     (object?)null
        
        Note: We use (object?)null because C# anonymous types
        cannot infer the type from just 'null'.
        """
        return "(object?)null"
    
    def visit_identifier(self, node: IdentifierExpr) -> str:
        """
        Convert Python identifier (variable reference).
        
        Python: user_id
        C#:     user_id
        """
        return node.name
    
    def visit_member_access(self, node: MemberAccessExpr) -> str:
        """
        Convert Python member access (body.name).
        
        Python: body.name
        C#:     body.name
        """
        return f"{node.object_name}.{node.member_name}"
    
    def visit_dict(self, node: DictExpr) -> str:
        """
        Convert Python dict to C# anonymous object.
        
        Python: {"name": "John", "age": 30}
        C#:     new { name = "John", age = 30 }
        """
        if not node.items:
            return "new { }"
        
        items = []
        for item in node.items:
            key = item.key
            value = self.visit_expression(item.value)
            items.append(f"{key} = {value}")
        
        return "new { " + ", ".join(items) + " }"
    
    def visit_list(self, node: ListExpr) -> str:
        """
        Convert Python list to C# array.
        
        Python: [1, 2, 3]
        C#:     new[] { 1, 2, 3 }
        
        Empty list:
        Python: []
        C#:     Array.Empty<object>()
        """
        if not node.items:
            return "Array.Empty<object>()"
        
        items = [self.visit_expression(item) for item in node.items]
        return "new[] { " + ", ".join(items) + " }"


# ==============================================================================
# Convenience Function
# ==============================================================================

def generate_csharp(program: ProgramNode) -> str:
    """
    Convenience function to generate C# code from AST.
    
    Usage:
        from dukpyra.codegen import generate_csharp
        csharp_code = generate_csharp(ast)
    """
    generator = CSharpCodeGenerator()
    return generator.generate(program)
