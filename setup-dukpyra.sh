#!/bin/bash
# =============================================================================
# Dukpyra Complete Setup Script
# สคริปต์สร้างโครงสร้างโปรเจกต์ทั้งหมด
# =============================================================================

echo "🚀 Setting up Dukpyra Compiler Project..."

# 1. สร้างโครงสร้างโฟลเดอร์
mkdir -p dukpyra-compiler
cd dukpyra-compiler

mkdir -p dukpyra/templates
mkdir -p tests
mkdir -p examples

echo "📁 Created project structure"

# 2. สร้างไฟล์ __init__.py
cat > dukpyra/__init__.py << 'EOF'
"""
Dukpyra - Python to ASP.NET Core Compiler
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .lexer import lexer
from .parser import parser

__all__ = ['lexer', 'parser', '__version__']
EOF

# 3. สร้าง setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dukpyra",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python to ASP.NET Core Compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dukpyra",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ply>=3.11",
        "watchdog>=3.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dukpyra=dukpyra.cli:main",
        ],
    },
    include_package_data=True,
)
EOF

# 4. สร้าง requirements.txt
cat > requirements.txt << 'EOF'
ply>=3.11
watchdog>=3.0.0
click>=8.0.0
EOF

# 5. สร้าง requirements-dev.txt
cat > requirements-dev.txt << 'EOF'
-r requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
EOF

# 6. สร้าง .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Dukpyra specific
.dukpyra/
*.csproj
*.cs

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
EOF

# 7. สร้าง README.md
cat > README.md << 'EOF'
# 🚀 Dukpyra

**Python to ASP.NET Core Compiler**

แปลง Python Web Framework (Flask/FastAPI style) ให้เป็น ASP.NET Core Minimal API อัตโนมัติ

## ✨ Features

- 🔥 Hot reload - แก้โค้ดแล้ว server รีสตาร์ทเอง
- 📦 Hidden compilation - เห็นแค่ Python, รันด้วย C#
- ⚡ High performance - ใช้ความเร็วของ ASP.NET Core
- 🎯 Simple syntax - เขียน Python แบบธรรมดา

## 📦 Installation

```bash
pip install dukpyra
```

## 🚀 Quick Start

```bash
# สร้างโปรเจกต์ใหม่
dukpyra init my-backend

# เข้าไปในโฟลเดอร์
cd my-backend

# รันโปรเจกต์
dukpyra run
```

## 📝 Example

**main.py:**
```python
@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/users/{id}")
def get_user():
    return {"id": 123, "name": "John"}
```

**Compiled to C#:**
```csharp
app.MapGet("/", () =>
{
    return Results.Ok(new { message = "Hello World" });
});

app.MapGet("/users/{id}", () =>
{
    return Results.Ok(new { id = 123, name = "John" });
});
```

## 📚 Commands

| Command | Description |
|---------|-------------|
| `dukpyra init <name>` | สร้างโปรเจกต์ใหม่ |
| `dukpyra run` | รันโปรเจกต์ (พร้อม hot reload) |
| `dukpyra show` | แสดงโค้ด C# ที่ compile แล้ว |
| `dukpyra clean` | ลบไฟล์ compiled |
| `dukpyra build` | Build production binary |
| `dukpyra info` | แสดงข้อมูลโปรเจกต์ |

## 🔧 Requirements

- Python 3.8+
- .NET 8.0 SDK

## 📖 Documentation

Visit [https://dukpyra.dev](https://dukpyra.dev) for full documentation.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PLY (Python Lex-Yacc) for lexer/parser
- ASP.NET Core team for amazing framework
- FastAPI for inspiration

---

Made with ❤️ by [Your Name]
EOF

# 8. สร้าง LICENSE (MIT)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 9. สร้าง MANIFEST.in
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
include requirements.txt
recursive-include dukpyra/templates *
EOF

# 10. สร้าง example project
mkdir -p examples/simple-api
cat > examples/simple-api/main.py << 'EOF'
# Simple API Example

@app.get("/")
def home():
    return {"message": "Welcome to Dukpyra API", "version": "1.0"}

@app.get("/users")
def list_users():
    return {"users": ["Alice", "Bob", "Charlie"], "count": 3}

@app.post("/users")
def create_user():
    return {"id": 1, "name": "New User", "created": "true"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "uptime": 12345}
EOF

# 11. สร้าง test file ตัวอย่าง
cat > tests/test_lexer.py << 'EOF'
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
EOF

cat > tests/test_cli.py << 'EOF'
import pytest
from click.testing import CliRunner
from dukpyra.cli import cli

def test_cli_version():
    """Test version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output

def test_cli_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Dukpyra' in result.output
EOF

# 12. สร้าง pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --cov=dukpyra --cov-report=html --cov-report=term
EOF

# 13. สร้าง pyproject.toml (modern Python)
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
EOF

# 14. สร้าง Makefile (optional)
cat > Makefile << 'EOF'
.PHONY: install dev test clean build publish

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

test:
	pytest

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

publish:
	python -m twine upload dist/*

format:
	black dukpyra tests

lint:
	flake8 dukpyra tests
	mypy dukpyra
EOF

echo ""
echo "✅ Project structure created successfully!"
echo ""
echo "📁 Structure:"
echo "   dukpyra-compiler/"
echo "   ├── dukpyra/           # Main package"
echo "   │   ├── __init__.py"
echo "   │   ├── cli.py         # ← วางโค้ด CLI ของคุณ"
echo "   │   ├── lexer.py       # ← วางโค้ด Lexer ของคุณ"
echo "   │   ├── parser.py      # ← วางโค้ด Parser ของคุณ"
echo "   │   └── templates/"
echo "   ├── tests/             # Test files"
echo "   ├── examples/          # Example projects"
echo "   ├── setup.py"
echo "   ├── requirements.txt"
echo "   └── README.md"
echo ""
echo "🔧 Next steps:"
echo "   1. cd dukpyra-compiler"
echo "   2. วางไฟล์ lexer.py, parser.py, cli.py ลงใน dukpyra/"
echo "   3. pip install -e ."
echo "   4. dukpyra --version"
echo ""
echo "🚀 Ready to compile!"
