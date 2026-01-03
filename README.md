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

This project is developed as part of a **compiler construction research** exploring **runtime type collection and transpilation from dynamic to static languages**, based on the methodology of **P. Krivanek and R. Uttner**.

### Core Research Question

**How can we transpile Python (dynamic typing) to C# (static typing) accurately using runtime type profiling?**

The answer: Collect actual type information during runtime execution and use it to generate precisely-typed C# code - a technique documented in *"Runtime type collecting and transpilation to a static language"*.

### Research Objectives

| Objective | Description | Status |
|-----------|-------------|---------|
| **RO1** | Design a lexer and parser for Python API syntax using PLY | ✅ Complete |
| **RO2** | Implement an Abstract Syntax Tree (AST) representation | ✅ Complete |
| **RO3** | Create a semantic analyzer for validation | ✅ Complete |
| **RO4** | Generate correct C# code from AST with runtime type data | ✅ Complete |
| **RO5** | Evaluate the transpiler with real-world API patterns | 🔄 In Progress |

### Scope & Limitations

**In Scope:**
- HTTP methods: GET, POST, PUT, DELETE, PATCH
- Path and query parameters with type hints
- Request/response bodies via class definitions
- **Runtime type profiling** for dynamic code
- Basic data types: int, str, float, bool, list, dict
- Nested type inference: `List[int]`, `Dict[str, User]`
- Semantic validation: duplicates, undefined refs, type checking

**Out of Scope:**
- Full Python language support (only API subset)
- Async/await patterns
- Middleware and dependency injection
- Database integration
- Authentication/Authorization

---

## 🔬 Runtime Type Collection Methodology

Dukpyra implements the **runtime type collection** approach from research literature:

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│         RUNTIME TYPE COLLECTION (Krivanek & Uttner)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Profile Runtime                                             │
│     ┌──────────────┐                                            │
│     │ Python Code  │───▶ Execute ───▶  Collect Types           │
│     │ (no hints)   │                   (.dukpyra/types.json)    │
│     └──────────────┘                                            │
│                                                                 │
│  2. Transpile with Type Data                                    │
│     ┌──────────────┐       ┌─────────────┐                     │
│     │ Python Code  │──────▶│  Compiler   │                     │
│     └──────────────┘   +   │  Pipeline   │───▶ C# Code         │
│     ┌──────────────┐       └─────────────┘                     │
│     │ types.json   │──────▶                                     │
│     └──────────────┘                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Type Inference Priority

1. **Runtime profiled types** (Primary) - from `.dukpyra/types.json`
2. **Static type hints** (Fallback) - from source code annotations
3. **Dynamic type** (Last resort) - C# `dynamic` keyword

### Example

```python
# Python code WITHOUT type hints
@app.get("/process")
def process(numbers):  # ← No type hint!
    return [x * 2 for x in numbers]
```

```bash
# Step 1: Profile runtime
$ dukpyra profile
# Calls process([1, 2, 3]) → Detects: numbers = List[int]

# Step 2: Build
$ dukpyra build
```

```csharp
// Generated C# with runtime-inferred types
app.MapGet("/process", (List<int> numbers) =>
{
    return Results.Ok(numbers.Select(x => x * 2).ToList());
});
```

**Key Insight**: Even without type hints, Dukpyra infers `List<int>` from runtime observation!

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
│           │ (PLY)  │  │ (LALR) │  │     │  │          │  │ +types│ │
│           └────────┘  └────────┘  └─────┘  └──────────┘  └──────┘ │
│                                                 ▲            │     │
│                                                 │            │     │
│                          Runtime Profiler ─────┘            │     │
│                          (.dukpyra/types.json)              │     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

| Stage | File | Lines | Description |
|-------|------|-------|-------------|
| Lexer | `lexer.py` | ~500 | Tokenizes Python source | 
| Parser | `parser.py` | ~450 | Builds AST using LALR(1) grammar |
| AST | `ast.py` | ~700 | Node definitions with detailed docs |
| Analyzer | `analyzer.py` | ~300 | Semantic validation |
| CodeGen | `codegen.py` | ~330 | Generates C# from AST + runtime types |
| **Runtime** | `runtime.py` | ~400 | **Type collection during execution** |

**Total: ~2,700 lines of code**

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

# ✨ NEW: Runtime type profiling
@app.get("/active-users")
def get_active_users(users):  # No type hint needed!
    # Dukpyra profiles this at runtime and infers: List[User]
    return [u.name for u in users if u.active]
```

### Feature Matrix

| Feature | Status | Example |
|---------|--------|---------|
| GET/POST/PUT/DELETE/PATCH | ✅ | `@app.get("/path")` |
| Path Parameters | ✅ | `/users/{id}` |
| Query Parameters | ✅ | `def search(q: str):` |
| Type Hints (Static) | ✅ | `int`, `str`, `float`, `bool` |
| **Runtime Type Profiling** | ✅ NEW | `dukpyra profile` |
| **Nested Type Inference** | ✅ NEW | `List[int]`, `Dict[str, User]` |
| **Custom Class Detection** | ✅ NEW | Auto-detect `User`, `Product` |
| Request Bodies | ✅ | `class Model:` → C# record |
| LINQ Generation | ✅ | `[x for x in list]` → `list.Select(...)` |
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

## 🚀 Quick Start

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

# 🆕 Profile runtime types (recommended workflow)
dukpyra profile

# Run development server with hot reload
dukpyra run

# Build only (no run) 
dukpyra build

# Clean generated files
dukpyra clean
```

### Recommended Workflow

```bash
# 1. Write Python code (with or without type hints)
vim main.py

# 2. Profile to collect runtime types
dukpyra profile
# ↑ Runs your code and saves type data to .dukpyra/types.json

# 3. Build (uses profiled types for better inference)
dukpyra build

# 4. Run
cd build
dotnet run
```

---

## 📊 Type Mapping

### Basic Types

| Python | C# |
|--------|-----|
| `str` | `string` |
| `int` | `int` |
| `float` | `double` |
| `bool` | `bool` |
| `None` | `null` |

### Collections (NEW - Enhanced)

| Python | C# (Runtime Profiled) |
|--------|----------------------|
| `[1, 2, 3]` | `List<int>` |
| `["a", "b"]` | `List<string>` |
| `[User(), User()]` | `List<User>` |
| `{"name": "John", "age": 30}` | `Dictionary<string, dynamic>` |

### Custom Types

| Python | C# |
|--------|-----|
| `class User: ...` | `public record User(...)` |

---

## 🔜 Future Work

### Short Term
- [ ] Enhanced type conflict resolution (when function called with different types)
- [ ] Default parameter values
- [ ] Negative numbers in lexer
- [ ] Response type annotations

### Medium Term
- [ ] HTTP status codes
- [ ] Confidence scoring for profiled types
- [ ] Generator expressions
- [ ] Error handling patterns

### Long Term
- [ ] Async/await support
- [ ] Benchmark suite (evaluate RO5)
- [ ] User study for compiler usability
- [ ] Multi-target code generation (TypeScript, Go, Rust)

---

## 📁 Project Structure

```
Dukpyra/
├── dukpyra-compiler/          # Compiler source
│   └── dukpyra/
│       ├── lexer.py           # Tokenizer (~500 lines)
│       ├── parser.py          # Grammar → AST (~450 lines)
│       ├── ast.py             # AST node definitions (~700 lines)
│       ├── analyzer.py        # Semantic analysis (~300 lines)
│       ├── codegen.py         # AST → C# (~330 lines)
│       ├── runtime.py         # 🆕 Runtime type profiler (~400 lines)
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

## 📄 License

MIT License

---

## 👨‍💻 Author

**Rock** - Compiler Design Research Project

---

## 🧙‍♂️ Why "Dukpyra"?

> **Duk** (ดุ๊ก) + **Py**thon + C sha**rp** = **Dukpyra** 🔮

---

## 📚 Research Reference

**Primary Reference:**

P. Krivanek and R. Uttner, "Runtime type collecting and transpilation to a static language," *CEUR Workshop Proceedings*, vol. 3893, 2024.  
[[PDF]](https://ceur-ws.org/Vol-3893/Paper08.pdf)

### Citation

```bibtex
@inproceedings{krivanek2024runtime,
  title={Runtime type collecting and transpilation to a static language},
  author={Krivanek, P. and Uttner, R.},
  booktitle={CEUR Workshop Proceedings},
  volume={3893},
  year={2024},
  url={https://ceur-ws.org/Vol-3893/Paper08.pdf}
}
```

### Key Contributions from Research

1. **Runtime Type Collection**: Profiling actual values during execution
2. **Dynamic-to-Static Conversion**: Using profiled data for static typing
3. **Documented Limitations**: Stateful traits, metaprogramming constraints
4. **Practical Application**: Web API domain focus for controlled scope

---

<p align="center">
  <b>Version 0.3.0 - Research Build</b><br>
  Implementing Runtime Type Collection Methodology
</p>
