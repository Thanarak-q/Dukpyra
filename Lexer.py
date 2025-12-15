import ply.lex as lex

# ==============================================================================
# ส่วนที่ 1: LEXER (ตัวตัดคำ)
# หน้าที่หลัก: เปรียบเสมือน "คนอ่านหนังสือ" ที่จะไล่อ่านโค้ดทีละตัวอักษร
# แล้วจับกลุ่มคำออกมาเป็นชิ้นๆ ที่เรียกว่า "Token" เพื่อส่งต่อให้ Parser
# ==============================================================================

# 1.1 คำสงวน (Reserved Words)
# คือคำที่มีความหมายเฉพาะในภาษา Python หรือ Framework ห้ามนำไปตั้งชื่อตัวแปร
# เราใช้ Dictionary เพื่อจับคู่คำศัพท์ (Key) กับชื่อ Token (Value)
reserved = {
    "def": "DEF",  # ใช้สำหรับประกาศฟังก์ชัน
    "return": "RETURN",  # คำสั่งส่งค่ากลับจากฟังก์ชัน
    "get": "GET",  # คำสั่ง HTTP Method GET
    "post": "POST",  # คำสั่ง HTTP Method POST
    "app": "APP",  # ชื่อตัวแปร app (Web Application)
    # ประเภทตัวแปร (Data Types) - เพิ่มกลับมาให้แล้วครับ
    "int": "TYPE_INT",
    "str": "TYPE_STR",
    "float": "TYPE_FLOAT",
    "bool": "TYPE_BOOL",
}

# 1.2 รายชื่อ Token ทั้งหมด (Token List)
# เป็นบัญชีรายชื่อที่ Lexer ต้องรู้จัก ทั้งแบบสัญลักษณ์และคำสงวน
tokens = [
    "ID",  # Identifier: ชื่อตัวแปร หรือชื่อฟังก์ชันที่ผู้ใช้ตั้งเอง
    "STRING",  # String: ข้อความตัวอักษรที่อยู่ในเครื่องหมายคำพูด ""
    "LPAREN",  # Left Parenthesis: วงเล็บเปิด (
    "RPAREN",  # Right Parenthesis: วงเล็บปิด )
    "LBRACE",  # Left Brace: ปีกกาเปิด { (ใช้กับ Dictionary / JSON)
    "RBRACE",  # Right Brace: ปีกกาปิด }
    "COLON",  # Colon: เครื่องหมายโคลอน :
    "COMMA",  # Comma: เครื่องหมายจุลภาค ,
    "AT",  # At sign: เครื่องหมาย @ (ใช้สำหรับ Decorator)
    "DOT",  # Dot: จุด .
    "NEWLINE",  # Newline: การขึ้นบรรทัดใหม่ (สำคัญมากใน Python)
] + list(reserved.values())  # นำรายชื่อคำสงวนมารวมเข้าไปใน List นี้ด้วย

# 1.3 กฎการตัดคำแบบง่าย (Simple Regex Rules)
# ใช้ Regular Expression เพื่อจับคู่สัญลักษณ์พิเศษเข้ากับชื่อ Token
t_LPAREN = r"\("  # ถ้าเจอ ( ให้ระบุว่าเป็น Token LPAREN
t_RPAREN = r"\)"  # ถ้าเจอ ) ให้ระบุว่าเป็น Token RPAREN
t_LBRACE = r"\{"  # ถ้าเจอ { ให้ระบุว่าเป็น Token LBRACE
t_RBRACE = r"\}"  # ถ้าเจอ } ให้ระบุว่าเป็น Token RBRACE
t_COLON = r":"  # ถ้าเจอ : ให้ระบุว่าเป็น Token COLON
t_COMMA = r","  # ถ้าเจอ , ให้ระบุว่าเป็น Token COMMA
t_AT = r"@"  # ถ้าเจอ @ ให้ระบุว่าเป็น Token AT
t_DOT = r"\."  # ถ้าเจอ . ให้ระบุว่าเป็น Token DOT

# สิ่งที่ให้มองข้าม (Ignored characters)
# เราจะข้ามช่องว่าง (Space) และแท็บ (Tab) ไปเลย ไม่เอามาทำเป็น Token
t_ignore = " \t"

# 1.4 กฎการตัดคำแบบซับซ้อน (Function Rules)
# ใช้ฟังก์ชันเมื่อต้องการ Logic เพิ่มเติม เช่น การแปลงค่า หรือการเช็คคำสงวน


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    # กฎนี้จับคำภาษาอังกฤษ (เช่น my_func, app, def)
    # Logic: เมื่อเจอคำ ให้เช็คใน dict 'reserved' ก่อน
    # - ถ้ามีใน reserved (เช่น 'def') -> ให้เป็น Token ประเภทนั้น (DEF)
    # - ถ้าไม่มี (เช่น 'my_func') -> ให้เป็น Token ประเภท ID
    t.type = reserved.get(t.value, "ID")
    return t


def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""
    # กฎนี้จับข้อความในเครื่องหมายคำพูดคู่ (เช่น "hello")
    # เราต้องตัดเครื่องหมายคำพูด " หัวและท้ายออก เพื่อเอาเฉพาะเนื้อหาข้างใน
    # ตัวอย่าง: "hello" -> hello
    t.value = t.value[1:-1]
    return t


def t_NEWLINE(t):
    r"\n+"
    # กฎนี้จับการกด Enter (ขึ้นบรรทัดใหม่)
    # เราต้องนับบรรทัด (lineno) เพิ่มขึ้น เพื่อใช้บอกตำแหน่งเวลาเกิด Error
    t.lexer.lineno += len(t.value)
    return t


# ฟังก์ชันจัดการ Error (Error Handling)
# จะทำงานเมื่อเจอตัวอักษรที่ไม่อยู่ในกฎข้างบนเลย
def t_error(t):
    print(f"Lexer Error: เจอตัวอักษรที่ไม่รู้จัก '{t.value[0]}' ที่บรรทัด {t.lexer.lineno}")
    t.lexer.skip(1)  # ข้ามตัวที่มีปัญหาไป 1 ตัวแล้วทำงานต่อ


# สร้าง Lexer Object
# คำสั่งนี้จะรวบรวมกฎทั้งหมดข้างบนมาสร้างเป็นตัวตัดคำ พร้อมใช้งาน
lexer = lex.lex()
