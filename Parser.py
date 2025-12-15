import ply.yacc as yacc

# นำเข้า tokens และ lexer จากไฟล์ lexer.py ที่เราแยกไว้
# จำเป็นต้องมีไฟล์ lexer.py อยู่ในโฟลเดอร์เดียวกัน
from Lexer import lexer, tokens

# ==============================================================================
# ส่วนที่ 2: PARSER (ตัวตรวจไวยากรณ์และแปลภาษา)
# หน้าที่หลัก: เปรียบเสมือน "คนเรียบเรียงประโยค" ที่จะนำ Token มาต่อกันตามกฎ
# แล้วแปลงร่าง (Translation) ให้กลายเป็นโค้ดภาษาปลายทาง (C#)
# ==============================================================================


# 2.1 กฎเริ่มต้น (Start Symbol)
# จุดเริ่มต้นของการทำงานทั้งหมด โปรแกรมจะเริ่มมองหาจากกฎนี้เป็นที่แรก
def p_program(p):
    """program : endpoints"""
    # p[1] คือเนื้อหาโค้ดส่วน Route ทั้งหมดที่ถูกแปลงเสร็จแล้วจากกฎ endpoints

    # ส่วนหัวของไฟล์ C# (Boilerplate Code) ที่จำเป็นสำหรับ Minimal API
    header = """var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// --- Dukpyra Generated Routes ---
"""
    # ส่วนท้ายของไฟล์ C# เพื่อสั่งรัน Server
    footer = """
// --------------------------------

app.Run();"""

    # นำหัว + ไส้ใน + ท้าย มารวมกันเป็นไฟล์สมบูรณ์
    p[0] = header + p[1] + footer


# 2.2 กฎสำหรับจัดการ Endpoint หลายๆ ตัว (Recursive Rule)
# เพื่อให้รองรับการเขียน Route ได้ไม่จำกัดจำนวน โดยใช้หลักการเรียกตัวเองซ้ำ
def p_endpoints_multiple(p):
    """endpoints : endpoint endpoints"""
    # กรณีมีหลายตัว: เอา Endpoint ปัจจุบัน (p[1]) มาต่อกับ Endpoint ที่เหลือ (p[2])
    # คั่นด้วย \n\n เพื่อความสวยงาม
    p[0] = f"{p[1]}\n\n{p[2]}"


def p_endpoints_single(p):
    """endpoints : endpoint"""
    # กรณีเหลือ Endpoint ตัวสุดท้าย (Base case)
    p[0] = p[1]


# 2.3 กฎหัวใจหลัก: แปลง 1 Endpoint จาก Python -> C#
# โครงสร้าง: @Decorator ตามด้วย Function Definition
def p_endpoint(p):
    """endpoint : decorator function_def"""
    # p[1] รับค่า Tuple (Method, Url) มาจากกฎ decorator เช่น ("Get", "/api")
    method, url = p[1]

    # p[2] รับค่าไส้ในฟังก์ชัน (Return Statement) มาจากกฎ function_def
    body = p[2]

    # *** สร้างโค้ด C# Minimal API ***
    # นำ Method, URL และ Body มาประกอบร่างตาม Template ของ C#
    p[0] = f'app.Map{method}("{url}", () =>\n{{\n    {body}\n}});'


# 2.4 กฎสำหรับ Decorator (@app.get หรือ @app.post)
def p_decorator_get(p):
    """decorator : AT APP DOT GET LPAREN STRING RPAREN NEWLINE"""
    # ถ้าเจอแพทเทิร์น @app.get("...") ให้ส่งค่ากลับเป็น Tuple
    # p[6] คือตำแหน่งของ STRING (URL) ที่ Lexer ตัดมาให้
    p[0] = ("Get", p[6])


def p_decorator_post(p):
    """decorator : AT APP DOT POST LPAREN STRING RPAREN NEWLINE"""
    # ถ้าเจอแพทเทิร์น @app.post("...")
    p[0] = ("Post", p[6])


# 2.5 กฎสำหรับ Function Definition (def ...)
# เราสนใจเฉพาะสิ่งที่ฟังก์ชัน Return ออกไป เพื่อนำไปสร้าง Response ใน C#
def p_function_def(p):
    """function_def : DEF ID LPAREN RPAREN COLON NEWLINE RETURN expression NEWLINE"""
    # expression (p[8]) คือข้อมูลที่ถูก Return (อาจเป็น String หรือ Dict)
    # เราห่อมันด้วย Results.Ok(...) ตามมาตรฐาน ASP.NET Core
    p[0] = f"return Results.Ok({p[8]});"


# 2.6 กฎสำหรับ Expression (ข้อมูลที่ส่งกลับ)


# กรณีที่ 1: ส่งกลับเป็น String ธรรมดา
def p_expression_string(p):
    """expression : STRING"""
    # เติมเครื่องหมายคำพูดกลับเข้าไป เพราะใน C# ต้องเป็น "ข้อความ"
    p[0] = f'"{p[1]}"'


# กรณีที่ 2: ส่งกลับเป็น Dictionary (JSON)
# เราต้องแปลงจาก Python Dict { ... } เป็น C# Anonymous Object new { ... }
def p_expression_dict(p):
    """expression : LBRACE dict_items RBRACE"""
    # รูปแบบ C#: new { key = value, ... }
    p[0] = f"new {{ {p[2]} }}"


# กฎย่อยสำหรับไส้ใน Dictionary (หลายรายการ)
def p_dict_items_multiple(p):
    """dict_items : dict_item COMMA dict_items"""
    # เอาคู่ key=value ปัจจุบัน (p[1]) ต่อกับตัวที่เหลือ (p[3]) คั่นด้วย ,
    p[0] = f"{p[1]}, {p[3]}"


# กฎย่อยสำหรับไส้ใน Dictionary (รายการเดียว)
def p_dict_items_single(p):
    """dict_items : dict_item"""
    p[0] = p[1]


# กฎย่อยสำหรับ Key: Value
def p_dict_item(p):
    """dict_item : STRING COLON STRING"""
    # แปลงไวยากรณ์:
    # Python: "key": "value"
    # C#:      key = "value"  (Anonymous Object Property)
    # หมายเหตุ: p[1] จาก Lexer ถูกตัด quote ออกแล้ว จึงใช้เป็นชื่อ Property ได้เลย
    p[0] = f'{p[1]} = "{p[3]}"'


# ฟังก์ชันแจ้งเตือน Error ของ Parser (Syntax Error)
def p_error(p):
    if p:
        print(f"Parser Error: ไวยากรณ์ผิดพลาดที่คำว่า '{p.value}' บรรทัดที่ {p.lineno}")
    else:
        print("Parser Error: ไวยากรณ์ผิดพลาดที่จุดจบไฟล์ (EOF) - อาจลืมวงเล็บหรือบรรทัดใหม่")


# สร้าง Parser Object
parser = yacc.yacc()

# ==============================================================================
# ส่วนที่ 3: ทดสอบการทำงาน (Main Execution)
# ==============================================================================
if __name__ == "__main__":
    # จำลองโค้ด Python ที่ผู้ใช้เขียน
    python_code = """
@app.get("/")
def home():
    return {"message": "HI from dukpyra i am 4 year old"}

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0"}

@app.get("/test")
def test_route():
    return {"message": "test"}
"""

    print("--- โค้ด Python ต้นฉบับ ---")
    print(python_code)

    print("\n--- ผลลัพธ์ C# ASP.NET Core Minimal API ---")

    # หมายเหตุ: .strip() + "\n" เป็นเทคนิคสำคัญ
    # 1. .strip() ลบบรรทัดว่างหัว-ท้ายที่ไม่จำเป็น
    # 2. + "\n" เติมบรรทัดใหม่ตอนจบ เพื่อให้ตรงกฎ NEWLINE ที่ Parser รอรับ
    result = parser.parse(python_code.strip() + "\n", lexer=lexer)

    if result:
        print(result)
    else:
        print("เกิดข้อผิดพลาดในการแปลงโค้ด")
