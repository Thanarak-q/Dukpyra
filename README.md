# 🔮 Dukpyra

<p align="center">
  <img src="mascot.png" alt="Dukpyra Mascot" width="600">
</p>

> **Python-to-C# Transpiler for Web APIs**  
> เขียน API ด้วย Python syntax รันบน .NET runtime

[![Version](https://img.shields.io/badge/version-0.3.0-purple.svg)](https://github.com/Thanarak-q/Dukpyra)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8+-purple.svg)](https://dotnet.microsoft.com/)

---

## 📚 Research Context

This project is developed as part of a **compiler construction research** exploring the feasibility of:

1. **Cross-language transpilation** - Converting Python web API definitions to C# ASP.NET Core
2. **Domain-specific language design** - Creating a Python DSL for web API development
3. **Semantic analysis** - Implementing validation and error detection before code generation

### Research Objectives

| Objective | Description |
|-----------|-------------|
| **RO1** | Design a lexer and parser for Python API syntax using PLY |
| **RO2** | Implement an Abstract Syntax Tree (AST) representation |
| **RO3** | Create a semantic analyzer for validation |
| **RO4** | Generate correct C# code from AST |
| **RO5** | Evaluate the transpiler with real-world API patterns |

### Scope & Limitations

**In Scope:**
- HTTP methods: GET, POST, PUT, DELETE, PATCH
- Path and query parameters with type hints
- Request/response bodies via class definitions
- Basic data types: int, str, float, bool, list, dict
- Semantic validation: duplicates, undefined refs, type checking

**Out of Scope:**
- Full Python language support (only API subset)
- Async/await patterns
- Middleware and dependency injection
- Database integration
- Authentication/Authorization

---

## 🏗️ Architecture

Dukpyra implements a **5-stage compiler pipeline**:

```
┌────────────────────────────────────────────────────────────────────┐
│                   DUKPYRA COMPILER v0.3.0                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Python   ┌────────┐  ┌────────┐  ┌─────┐  ┌──────────┐  ┌──────┐ │
│  Source ─▶│ Lexer  │─▶│ Parser │─▶│ AST │─▶│ Analyzer │─▶│CodeGen│─▶ C#
│           │ (PLY)  │  │ (LALR) │  │     │  │          │  │      │ │
│           └────────┘  └────────┘  └─────┘  └──────────┘  └──────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

| Stage | File | Lines | Description |
|-------|------|-------|-------------|
| Lexer | `lexer.py` | 116 | Tokenizes Python source into tokens |
| Parser | `parser.py` | 450 | Builds AST using LALR(1) grammar |
| AST | `ast.py` | 330 | Node definitions (15 types) |
| Analyzer | `analyzer.py` | 300 | Semantic validation (7 error types) |
| CodeGen | `codegen.py` | 330 | Generates C# from AST |

**Total: ~2,100 lines of code**

---

## ✅ Current Features (v0.3.0)

### Supported Syntax

```python
# Python-style imports and app creation
import dukpyra
app = dukpyra.app()

# Request body classes → C# records
class CreateUser:
    name: str
    email: str
    age: int

# HTTP endpoints with decorators
@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id, "name": "John"}

@app.post("/users")
def create_user(body: CreateUser):
    return {"created": True, "name": body.name}
```

### Feature Matrix

| Feature | Status | Example |
|---------|--------|---------|
| GET/POST/PUT/DELETE/PATCH | ✅ | `@app.get("/path")` |
| Path Parameters | ✅ | `/users/{id}` |
| Query Parameters | ✅ | `def search(q: str):` |
| Type Hints | ✅ | `int`, `str`, `float`, `bool` |
| Request Bodies | ✅ | `class Model:` → C# record |
| Lists | ✅ | `[1, 2, 3]` → `new[] {...}` |
| Booleans | ✅ | `True`/`False` → `true`/`false` |
| None | ✅ | `None` → `null` |
| Semantic Analysis | ✅ | Error detection with line numbers |

### Semantic Validation

| Error Code | Description |
|------------|-------------|
| E001 | Duplicate class definition |
| E002 | Duplicate endpoint (method + path) |
| E003 | Duplicate property in class |
| E004 | Unknown type in class property |
| E010 | Path parameter not in function |
| E011 | Unknown type in parameter |
| E020 | Undefined variable reference |

---

## � Quick Start

### Prerequisites

- Python 3.9+
- .NET SDK 8+ ([Download](https://dotnet.microsoft.com/download))

### Installation

```bash
# Clone the repository
git clone https://github.com/Thanarak-q/Dukpyra.git
cd Dukpyra/dukpyra-compiler

# Install as CLI tool
pip install -e .
```

### Usage

```bash
# Initialize new project
dukpyra init

# Run development server with hot reload
dukpyra run

# Build only (no run)
dukpyra build

# Clean generated files
dukpyra clean
```

---

## 📊 Type Mapping

| Python | C# |
|--------|-----|
| `str` | `string` |
| `int` | `int` |
| `float` | `double` |
| `bool` | `bool` |
| `None` | `null` |
| `list` | `new[] {...}` |
| `dict` | `new {...}` |
| Custom class | `public record` |

---

## 🔜 Future Work

### Short Term
- [ ] Default parameter values
- [ ] Negative numbers
- [ ] Response type annotations

### Medium Term
- [ ] HTTP status codes
- [ ] Middleware support
- [ ] Error handling patterns

### Long Term
- [ ] Async/await support
- [ ] Database integration
- [ ] Swagger generation

---

## 📁 Project Structure

```
Dukpyra/
├── dukpyra-compiler/          # Compiler source
│   └── dukpyra/
│       ├── lexer.py           # Tokenizer
│       ├── parser.py          # Grammar → AST
│       ├── ast.py             # AST node definitions
│       ├── analyzer.py        # Semantic analysis
│       ├── codegen.py         # AST → C#
│       └── cli.py             # CLI commands
├── my-test-backend/           # Example project
│   └── main.py                # Sample API
└── README.md
```

---

## 🧪 Testing

```bash
# Run with test backend
cd my-test-backend
dukpyra run

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/users/123
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@test.com","age":30}'
```

---

## � License

MIT License

---

## 👨‍💻 Author

**Rock** - Compiler Design Research Project

---

## 🧙‍♂️ Why "Dukpyra"?

> **Duk** (ดุ๊ก) + **Py**thon + C sha**rp** = **Dukpyra** 🔮

---

<p align="center">
  <b>Version 0.3.0 - Research Build</b>
</p>
