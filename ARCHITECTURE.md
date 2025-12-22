# Dukpyra Compiler Architecture

> **Python-to-C# Transpiler for Web APIs**

---

## Overview

Dukpyra implements a **5-stage compiler pipeline** that transforms Python web API definitions into executable C# ASP.NET Core Minimal API code.

```mermaid
flowchart LR
    A["Python Source<br/>(main.py)"] --> B["Lexer<br/>(PLY)"]
    B --> C["Parser<br/>(LALR)"]
    C --> D["AST"]
    D --> E["Semantic<br/>Analyzer"]
    E --> F["Code<br/>Generator"]
    F --> G["C# Output<br/>(Program.cs)"]
    
    style A fill:#3776AB,color:white
    style G fill:#68217A,color:white
```

---

## Component Details

### Stage 1: Lexer (`lexer.py`)

| Property | Value |
|----------|-------|
| **Lines** | 135 |
| **Library** | PLY (Python Lex-Yacc) |
| **Function** | Tokenizes source code into tokens |

**Token Categories:**
- **Keywords:** `import`, `def`, `class`, `return`, `for`, `in`, `if`
- **HTTP Methods:** `get`, `post`, `put`, `delete`, `patch`
- **Type Hints:** `int`, `str`, `float`, `bool`
- **Literals:** `True`, `False`, `None`, `NUMBER`, `STRING`
- **Operators:** `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`

```python
# Input
@app.get("/users/{id}")

# Lexer Output
[AT, ID("app"), DOT, GET, LPAREN, STRING("/users/{id}"), RPAREN, NEWLINE]
```

---

### Stage 2: Parser (`parser.py`)

| Property | Value |
|----------|-------|
| **Lines** | 508 |
| **Algorithm** | LALR(1) |
| **Grammar Rules** | 76 productions |

**Grammar Structure:**

```
program         → preamble class_definitions endpoints
preamble        → import_stmt app_creation
class_definition → CLASS ID COLON NEWLINE properties
endpoint        → decorator function_def
decorator       → AT ID DOT METHOD LPAREN STRING RPAREN
function_def    → DEF ID LPAREN params RPAREN COLON NEWLINE RETURN expr
```

---

### Stage 3: AST (`ast.py`)

| Property | Value |
|----------|-------|
| **Lines** | 377 |
| **Node Types** | 19 dataclasses |
| **Pattern** | Composite Pattern |

**AST Hierarchy:**

```mermaid
classDiagram
    Node <|-- ProgramNode
    Node <|-- ImportNode
    Node <|-- AppCreationNode
    Node <|-- ClassDefNode
    Node <|-- GenericEndpointNode
    Node <|-- FunctionDefNode
    Node <|-- ExpressionNode
    
    ExpressionNode <|-- StringExpr
    ExpressionNode <|-- NumberExpr
    ExpressionNode <|-- BoolExpr
    ExpressionNode <|-- DictExpr
    ExpressionNode <|-- ListExpr
    ExpressionNode <|-- ListCompNode
    ExpressionNode <|-- IdentifierExpr
    ExpressionNode <|-- MemberAccessExpr
    ExpressionNode <|-- BinaryOpExpr
    
    ClassDefNode o-- ClassPropertyNode
    GenericEndpointNode o-- FunctionDefNode
    FunctionDefNode o-- ParameterNode
    DictExpr o-- DictItemNode
```

**Key Nodes:**

| Node | Purpose |
|------|---------|
| `ProgramNode` | Root node containing all definitions |
| `GenericEndpointNode` | Platform-agnostic endpoint (method + path + handler) |
| `ClassDefNode` | Request/Response body class |
| `ListCompNode` | List comprehension for LINQ generation |

---

### Stage 4: Semantic Analyzer (`analyzer.py`)

| Property | Value |
|----------|-------|
| **Lines** | 372 |
| **Error Types** | 7 |
| **Pattern** | Visitor Pattern |

**Validation Rules:**

| Code | Error Type | Example |
|------|------------|---------|
| E001 | Duplicate class definition | `class User` defined twice |
| E002 | Duplicate endpoint | Same `GET /users` twice |
| E003 | Duplicate property in class | `name: str` appears twice |
| E004 | Unknown type in class property | `age: xyz` |
| E010 | Path parameter not in function | `/users/{id}` but no `id` param |
| E011 | Unknown type in parameter | `def get(x: unknown)` |
| E020 | Undefined variable reference | Using `x` not in scope |

**Symbol Table:**
```python
@dataclass
class SymbolTable:
    classes: Dict[str, ClassDefNode]      # class_name → node
    endpoints: Dict[str, EndpointNode]    # "GET /path" → node
    builtin_types: Set[str]               # {"int", "str", "float", "bool", "list", "dict"}
```

---

### Stage 5: Code Generator (`codegen.py`)

| Property | Value |
|----------|-------|
| **Lines** | 277 |
| **Template Engine** | Jinja2 |
| **Pattern** | Visitor Pattern |

**Type Mapping:**

| Python | C# |
|--------|-----|
| `str` | `string` |
| `int` | `int` |
| `float` | `double` |
| `bool` | `bool` |
| `None` | `null` |
| `True`/`False` | `true`/`false` |
| `list` | `new[] {...}` |
| `dict` | `new {...}` |
| Custom class | `public record` |

**LINQ Transformation:**
```python
# Python (List Comprehension)
[u.name for u in users if u.active]

# C# (LINQ)
users.Where(u => u.active).Select(u => u.name).ToList()
```

**Template (`Program.cs.j2`):**
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

{% for class_record in classes %}
{{ class_record }}
{% endfor %}

{% for endpoint in endpoints %}
app.Map{{ endpoint.method }}("{{ endpoint.path }}", ({{ endpoint.params }}) =>
{
    {{ endpoint.body }}
});
{% endfor %}

app.Run();
```

---

## Data Flow Example

**Input (`main.py`):**
```python
import dukpyra
app = dukpyra.app()

class CreateUser:
    name: str
    age: int

@app.post("/users")
def create_user(body: CreateUser):
    return {"created": True, "name": body.name}
```

**Output (`Program.cs`):**
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

public record CreateUser(string Name, int Age);

app.MapPost("/users", (CreateUser body) =>
{
    return new { created = true, name = body.Name };
});

app.Run();
```

---

## File Statistics

| File | Lines | Responsibility |
|------|-------|----------------|
| `lexer.py` | 135 | Tokenization |
| `parser.py` | 508 | Grammar parsing |
| `ast.py` | 377 | Node definitions |
| `analyzer.py` | 372 | Semantic validation |
| `codegen.py` | 277 | C# generation |
| `cli.py` | ~400 | CLI interface |
| **Total** | **~2,100** | |

---

## Research Techniques Applied

| Technique | Reference | Implementation |
|-----------|-----------|----------------|
| Rule-driven AST rewriting | [1] | Parser + CodeGen |
| Templates + Transformation synergy | [5] | Jinja2 templates |
| Runtime Type Collection | [6] | Type hints → C# types |
| User-guided "Last Mile" | [4] | Raw C# injection |
| High-Level IR Optimization | [7] | List Comp → LINQ |

---

## Architecture Diagram (Full)

```mermaid
flowchart TB
    subgraph Input
        SRC["main.py<br/>Python Source"]
    end
    
    subgraph "Compiler Pipeline"
        subgraph Frontend
            LEX["lexer.py<br/>━━━━━━━━━<br/>PLY Lexer<br/>135 lines"]
            PAR["parser.py<br/>━━━━━━━━━<br/>LALR(1) Parser<br/>508 lines"]
        end
        
        subgraph "IR"
            AST["ast.py<br/>━━━━━━━━━<br/>19 Node Types<br/>377 lines"]
        end
        
        subgraph Backend
            ANA["analyzer.py<br/>━━━━━━━━━<br/>Semantic Analysis<br/>372 lines"]
            GEN["codegen.py<br/>━━━━━━━━━<br/>Code Generation<br/>277 lines"]
            TPL["Program.cs.j2<br/>━━━━━━━━━<br/>Jinja2 Template"]
        end
    end
    
    subgraph Output
        OUT["Program.cs<br/>C# ASP.NET Core"]
    end
    
    SRC --> LEX
    LEX -->|Tokens| PAR
    PAR -->|AST| AST
    AST --> ANA
    ANA -->|Validated AST| GEN
    GEN --> TPL
    TPL --> OUT
    
    style SRC fill:#3776AB,color:white
    style OUT fill:#68217A,color:white
    style AST fill:#f9f,stroke:#333
```
