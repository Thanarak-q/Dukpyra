# 🔮 Dukpyra

> **Python → C# JIT Compiler for Web APIs**  
> เขียน API ด้วย Python syntax รันด้วย .NET performance

[![Version](https://img.shields.io/badge/version-0.00001-purple.svg)](https://github.com/dukpyra)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-10-purple.svg)](https://dotnet.microsoft.com/)

---

## 🤔 What is Dukpyra?

**Dukpyra** คือ transpiler ที่แปลง Python code ไปเป็น C# ASP.NET Core แบบ real-time 

เขียน API แบบนี้ใน Python:

```python
@app.get("/")
def index():
    return {"message": "Hello from Dukpyra! 🔮"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0"}
```

แล้ว Dukpyra จะ **compile เป็น C#** และรันบน **.NET runtime** ให้อัตโนมัติ!

---

## ⚡ Features

| Feature | Description |
|---------|-------------|
| 🐍 **Python Syntax** | เขียน API ด้วย syntax ที่คุ้นเคย ไม่ต้องเรียน C# |
| 🚀 **.NET Performance** | รันบน ASP.NET Core ได้ performance ระดับ production |
| 🔥 **Hot Reload** | แก้ `input.py` แล้ว server reload อัตโนมัติ |
| 📦 **Zero Config** | `dukpyra init` แล้วเริ่มเขียนได้เลย |
| 🔄 **Type Mapping** | รองรับ Python type hints → C# types |

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- .NET SDK 10+ ([ดาวน์โหลด](https://dotnet.microsoft.com/download))

### 2. Install Dukpyra

```bash
# Clone or download the project
git clone https://github.com/rock/dukpyra.git
cd dukpyra

# Install as CLI tool (editable mode for development)
pip install -e .
```

### 3. Initialize Project

```bash
dukpyra init
```

### 4. Start Development Server

```bash
dukpyra dev
```

Server จะรันที่ `http://localhost:5000` 🎉

---

## 📝 Usage

### Available Commands

| Command | Description |
|---------|-------------|
| `dukpyra init` | สร้างโครงสร้างโปรเจกต์ใหม่ |
| `dukpyra dev` | รัน development server พร้อม hot reload |
| `dukpyra build` | Compile Python → C# |
| `dukpyra run` | รัน production server |
| `dukpyra clean` | ลบ generated files ทั้งหมด |
| `dukpyra version` | แสดงเวอร์ชัน |

### Options

```bash
# เปลี่ยน port
dukpyra dev --port 8080

# Enable HTTPS
dukpyra dev --https

# Skip initial build
dukpyra dev --no-build
```

---

## 🔧 How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  input.py   │ ──▶ │   compiler   │ ──▶ │   Program.cs    │
│  (Python)   │     │   (AST)      │     │   (C#)          │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  .NET Runtime   │
                                         │  (ASP.NET Core) │
                                         └─────────────────┘
```

1. **Parse** - อ่าน `input.py` และสร้าง AST (Abstract Syntax Tree)
2. **Transform** - แปลง Python constructs ไปเป็น C# equivalents
3. **Generate** - Render C# code ด้วย Jinja2 template
4. **Run** - รันบน .NET runtime ด้วย `dotnet run`

---

## 🗺️ Type Mapping

Dukpyra แปลง Python type hints ไปเป็น C# types อัตโนมัติ:

| Python | C# |
|--------|-----|
| `str` | `string` |
| `int` | `int` |
| `float` | `double` |
| `bool` | `bool` |
| `List[str]` | `List<string>` |
| `Optional[int]` | `int?` |
| `Dict[str, int]` | `Dictionary<string, int>` |
| `datetime` | `DateTime` |

---

## 📁 Project Structure

```
my-project/
├── input.py              # 📝 Your Python API definitions
├── cli.py                # 🛠️ Dukpyra CLI
├── compiler.py           # ⚙️ Python → C# compiler
└── services/             # 📦 Generated .NET project
    ├── Program.cs        # 🎯 Generated C# code
    ├── DukpyraApp.csproj # 📋 .NET project file
    └── ...
```

---

## 💡 Examples

### Basic GET Endpoint

```python
@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}
```

### With Parameters (Coming Soon)

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### POST Endpoint (Coming Soon)

```python
@app.post("/items")
def create_item(name: str, price: float):
    return {"name": name, "price": price}
```

---

## 🔜 Roadmap

- [ ] POST, PUT, DELETE methods
- [ ] Query parameters
- [ ] Request body parsing
- [ ] Middleware support
- [ ] Database integration
- [ ] Auto-generate Swagger docs
- [ ] Docker support

---

## 🤝 Contributing

Contributions are welcome! นี่คือ v0.00001 ยังมีอะไรให้ทำอีกเยอะ 😄

---

## 📄 License

MIT License

---

## 🧙‍♂️ Why "Dukpyra"?

> **Duk** (ดุ๊ก) + **Py**thon + C sha**rp** = **Dukpyra** 🔮

---

## 🌟 Vision

> **v0.00001** → เริ่มต้นจาก transpiler เล็กๆ  
> **v1.0.0** → กลายเป็น **Full-stack Framework** ที่ครบวงจร

เป้าหมายสุดท้ายของ Dukpyra คือการเป็น **framework เต็มรูปแบบ** ที่:

- 🎨 เขียน Backend ด้วย Python syntax
- ⚡ รันด้วย .NET 10 performance
- 🔌 มี ecosystem ของ plugins และ extensions
- 🛠️ รองรับ database, auth, caching, และอื่นๆ built-in
- 📦 Deploy ได้ทุกที่ด้วย Docker/K8s

**Stay tuned!** 🚀

---

<p align="center">
  <b>Made with 💜 by Rock</b>
</p>
