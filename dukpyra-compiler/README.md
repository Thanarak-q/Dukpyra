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
