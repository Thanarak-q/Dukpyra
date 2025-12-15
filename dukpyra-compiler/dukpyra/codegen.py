"""
Dukpyra Code Generator - AST to C# Transpiler

This module walks the AST and generates C# code for ASP.NET Core Minimal API.
It uses Jinja2 templates for the final code output.

Architecture:
    Source Code → Lexer → Parser → AST → CodeGen → C# Code (via Templates)
"""

import os
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader

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
    
    Uses the Visitor pattern to prepare data for Jinja2 templates.
    """
    
    def __init__(self):
        # Setup Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('Program.cs.j2')
    
    def generate(self, program: ProgramNode) -> str:
        """
        Generate complete C# code from a ProgramNode.
        
        Returns a complete Program.cs file content.
        """
        if program is None:
            return ""
        
        # Prepare data for template
        classes = [self.visit_class(c) for c in program.classes]
        endpoints = [self.visit_endpoint(e) for e in program.endpoints]
        
        # Render template
        return self.template.render(
            classes=classes,
            endpoints=endpoints
        )
    
    def visit_class(self, node: ClassDefNode) -> str:
        """
        Generate C# record type definition string.
        """
        params = []
        for prop in node.properties:
            csharp_type = self.python_type_to_csharp(prop.type_hint)
            params.append(f"{csharp_type} {prop.name}")
        
        params_str = ", ".join(params)
        return f"public record {node.name}({params_str});"
    
    def visit_endpoint(self, node: EndpointNode) -> Dict[str, str]:
        """
        Prepare endpoint data for template.
        """
        method = node.decorator.method.capitalize()
        path = node.decorator.path
        params = self.visit_params(node.function.params)
        body = self.visit_function_body(node.function)
        
        return {
            "method": method,
            "path": path,
            "params": params,
            "body": body
        }
    
    def visit_params(self, params: list) -> str:
        """
        Generate C# lambda parameter list string.
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
        """
        type_map = {
            "int": "int",
            "str": "string",
            "float": "double",
            "bool": "bool",
        }
        
        if python_type is None:
            return "dynamic"
        
        return type_map.get(python_type, python_type)
    
    def visit_function_body(self, node: FunctionDefNode) -> str:
        """
        Generate C# code for function body.
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
        # Escape special characters for C#
        escaped = node.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    
    def visit_number(self, node: NumberExpr) -> str:
        return str(node.value)
    
    def visit_bool(self, node: BoolExpr) -> str:
        return "true" if node.value else "false"
    
    def visit_none(self, node: NoneExpr) -> str:
        return "(object?)null"
    
    def visit_identifier(self, node: IdentifierExpr) -> str:
        return node.name
    
    def visit_member_access(self, node: MemberAccessExpr) -> str:
        return f"{node.object_name}.{node.member_name}"
    
    def visit_dict(self, node: DictExpr) -> str:
        if not node.items:
            return "new { }"
        
        items = []
        for item in node.items:
            key = item.key
            value = self.visit_expression(item.value)
            items.append(f"{key} = {value}")
        
        return "new { " + ", ".join(items) + " }"
    
    def visit_list(self, node: ListExpr) -> str:
        if not node.items:
            return "Array.Empty<object>()"
        
        items = [self.visit_expression(item) for item in node.items]
        return "new[] { " + ", ".join(items) + " }"


def generate_csharp(program: ProgramNode) -> str:
    """
    Convenience function to generate C# code from AST.
    """
    generator = CSharpCodeGenerator()
    return generator.generate(program)
