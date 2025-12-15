import ply.yacc as yacc

# นำเข้า tokens และ lexer จากไฟล์ lexer.py ที่เราแยกไว้
# จำเป็นต้องมีไฟล์ lexer.py อยู่ในโฟลเดอร์เดียวกัน
from .lexer import lexer, tokens

# ==============================================================================
# ส่วนที่ 2: PARSER & CODE GENERATOR
# หน้าที่หลัก: แปลง Token เป็นโค้ด C# ASP.NET Core Minimal API
#
# รองรับ syntax:
#   import dukpyra
#   app = dukpyra.app()
#   
#   @app.get("/")
#   def home():
#       return {"message": "Hello"}
# ==============================================================================


# 2.1 กฎเริ่มต้น (Start Symbol)
# program สามารถมี import statement และ app creation ก่อน endpoints
def p_program(p):
    """program : preamble endpoints"""
    # สร้าง Boilerplate Code ของ ASP.NET Core
    header = """var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// --- Dukpyra Generated Routes ---
"""
    footer = """
// --------------------------------

app.Run();"""
    p[0] = header + p[2] + footer


# 2.1.1 Preamble: import statements และ app creation (ถูกข้ามไปเพราะ C# ไม่ต้องการ)
def p_preamble_full(p):
    """preamble : optional_newlines import_stmt app_creation"""
    pass  # ไม่ต้องเก็บค่า เป็นแค่ Python syntax


def p_preamble_with_import(p):
    """preamble : optional_newlines import_stmt"""
    pass


def p_preamble_empty(p):
    """preamble : optional_newlines"""
    pass


# 2.1.2 Import Statement: import dukpyra
def p_import_stmt(p):
    """import_stmt : IMPORT ID NEWLINE optional_newlines"""
    pass  # ไม่ต้องแปลงเป็น C# 


# 2.1.3 App Creation: app = dukpyra.app()
def p_app_creation(p):
    """app_creation : ID EQUALS ID DOT ID LPAREN RPAREN NEWLINE optional_newlines"""
    pass  # ไม่ต้องแปลงเป็น C#


# 2.1.4 กฎสำหรับ newlines ที่อาจมีหรือไม่มีก็ได้
def p_optional_newlines_empty(p):
    """optional_newlines : """
    pass


def p_optional_newlines_some(p):
    """optional_newlines : NEWLINE optional_newlines"""
    pass


# 2.2 กฎสำหรับจัดการ Endpoint หลายๆ ตัว
def p_endpoints_multiple(p):
    """endpoints : endpoint endpoints"""
    p[0] = f"{p[1]}\n\n{p[2]}"


def p_endpoints_single(p):
    """endpoints : endpoint"""
    p[0] = p[1]


# 2.3 กฎแปลง Python Decorator & Function -> C# MapGet/Post/Put/Delete/Patch
def p_endpoint(p):
    """endpoint : decorator function_def"""
    method, url = p[1]
    body = p[2]
    # สร้างโค้ด Minimal API
    p[0] = f'app.Map{method}("{url}", () =>\n{{\n    {body}\n}});'


# 2.4 กฎสำหรับ Decorator - รองรับ @app.method("/path")
# ใช้ ID แทน APP เพื่อรองรับชื่อ app ที่ผู้ใช้ตั้งเอง
def p_decorator_get(p):
    """decorator : AT ID DOT GET LPAREN STRING RPAREN NEWLINE"""
    p[0] = ("Get", p[6])


def p_decorator_post(p):
    """decorator : AT ID DOT POST LPAREN STRING RPAREN NEWLINE"""
    p[0] = ("Post", p[6])


def p_decorator_put(p):
    """decorator : AT ID DOT PUT LPAREN STRING RPAREN NEWLINE"""
    p[0] = ("Put", p[6])


def p_decorator_delete(p):
    """decorator : AT ID DOT DELETE LPAREN STRING RPAREN NEWLINE"""
    p[0] = ("Delete", p[6])


def p_decorator_patch(p):
    """decorator : AT ID DOT PATCH LPAREN STRING RPAREN NEWLINE"""
    p[0] = ("Patch", p[6])


# 2.5 กฎสำหรับ Function Definition
def p_function_def(p):
    """function_def : DEF ID LPAREN RPAREN COLON NEWLINE RETURN expression NEWLINE"""
    # ใช้ expression ที่แปลงเป็น C# แล้วมาใส่ใน Ok()
    p[0] = f"return Results.Ok({p[8]});"


# 2.6 กฎสำหรับ Expression (ข้อมูลที่ส่งกลับ)
# รองรับทั้ง String, Number และ Dictionary ซ้อนกัน


def p_expression_string(p):
    """expression : STRING"""
    # เติมเครื่องหมายคำพูดสำหรับ C# string
    p[0] = f'"{p[1]}"'


def p_expression_number(p):
    """expression : NUMBER"""
    # แปลงตัวเลขเป็น String เพื่อใส่ในโค้ด (เช่น 123)
    p[0] = str(p[1])


def p_expression_dict(p):
    """expression : LBRACE dict_items RBRACE"""
    # แปลง Python Dict -> C# Anonymous Object
    # new { Key = Value, ... }
    p[0] = f"new {{ {p[2]} }}"


# กฎย่อยสำหรับไส้ใน Dictionary
def p_dict_items_multiple(p):
    """dict_items : dict_item COMMA dict_items"""
    p[0] = f"{p[1]}, {p[3]}"


def p_dict_items_single(p):
    """dict_items : dict_item"""
    p[0] = p[1]


def p_dict_item(p):
    """dict_item : STRING COLON expression"""
    # Key: มาจาก STRING (Lexer ตัด quote ออกแล้ว ใช้เป็นชื่อ Property ได้เลย)
    # Value: มาจาก expression (ซึ่งอาจเป็น "string", number, หรือ new { object })
    p[0] = f"{p[1]} = {p[3]}"


# Error Handling
def p_error(p):
    if p:
        print(f"Parser Error: ไวยากรณ์ผิดพลาดที่คำว่า '{p.value}' บรรทัดที่ {p.lineno}")
    else:
        print("Parser Error: ไวยากรณ์ผิดพลาดที่จุดจบไฟล์ (EOF)")


# สร้าง Parser Object
parser = yacc.yacc()

# ==============================================================================
# ส่วนที่ 3: ทดสอบการทำงาน (Main Execution)
# ==============================================================================
if __name__ == "__main__":
    # ทดสอบด้วย syntax ใหม่
    python_code = """
import dukpyra

app = dukpyra.app()

@app.get("/")
def home():
    return {"message": "Hello from Dukpyra!", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "uptime": 9999}

@app.post("/api/users")
def create_user():
    return {"id": 1, "name": "John Doe"}
"""

    print("--- โค้ด Python ต้นฉบับ ---")
    print(python_code)

    print("\n--- ผลลัพธ์ C# ASP.NET Core Minimal API ---")

    result = parser.parse(python_code.strip() + "\n", lexer=lexer)

    if result:
        print(result)
    else:
        print("เกิดข้อผิดพลาดในการแปลงโค้ด")
