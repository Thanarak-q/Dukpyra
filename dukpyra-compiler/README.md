# 🚀 Dukpyra

**Python to ASP.NET Core Compiler**

แปลง Python Web Framework (Flask/FastAPI style) ให้เป็น ASP.NET Core Minimal API อัตโนมัติ

## ✨ Features

- 🔥 Hot reload - แก้โค้ดแล้ว server รีสตาร์ทเอง
- 📦 Hidden compilation - เห็นแค่ Python, รันด้วย C#
- ⚡ High performance - ใช้ความเร็วของ ASP.NET Core
- 🎯 Simple syntax - เขียน Python แบบธรรมดา
- 💉 Raw C# Injection - แทรก C# code ได้เมื่อต้องการ
- 🎨 Template-based - ปรับแต่งโครงสร้างโค้ดได้ง่ายด้วย Jinja2

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

### 💉 Raw C# Injection

สำหรับกรณีที่ต้องการ Logic ที่ซับซ้อน หรือใช้ฟีเจอร์ของ .NET โดยตรง สามารถใช้ `@dukpyra.raw_csharp` ได้:

```python
@dukpyra.raw_csharp('Console.WriteLine("Debug Log"); return Results.Ok();')
@app.get("/debug")
def debug():
    return {"status": "ignored"}
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

## 🔬 Architecture & Research

โปรเจกต์นี้ได้รับการออกแบบโดยอ้างอิงงานวิจัยด้าน Compiler Engineering สมัยใหม่:

1.  **Templates and transformation synergy**: แยก Tramsformation Logic ออกจาก Code Generation โดยใช้ Template Engine (Jinja2) ตามแนวทางของ *Robert Eikermann et al. [5]* เพื่อการดูแลรักษาที่ง่ายและการปรับแต่งโครงสร้างที่ยืดหยุ่น
2.  **User-guided "Last Mile" construction**: แก้ปัญหาที่ Compiler แปลง Logic ซับซ้อนไม่ได้ทั้งหมดด้วยฟีเจอร์ "Raw C# Injection" ตามแนวคิดของ *DuoGlot (Bo Wang et al.) [4]* ที่เปิดช่องให้ผู้ใช้ช่วยเติมเต็มส่วนที่อัตโนมัติทำไม่ได้
3.  **Rule-driven AST rewriting**: ใช้พื้นฐานการแปลงแบบ Rule-based ตามมาตรฐานงานวิจัยของ *Lachaux et al. [1]* เพื่อความถูกต้องแม่นยำสูงสุด

---
