import ply.lex as lex

# ==============================================================================
# ส่วนที่ 1: LEXER (ตัวตัดคำ)
# หน้าที่หลัก: เปรียบเสมือน "คนอ่านหนังสือ" ที่จะไล่อ่านโค้ดทีละตัวอักษร
# แล้วจับกลุ่มคำออกมาเป็นชิ้นๆ ที่เรียกว่า "Token" เพื่อส่งต่อให้ Parser
# ==============================================================================

# 1.1 คำสงวน (Reserved Words)
# คือคำที่มีความหมายเฉพาะในภาษา Python หรือ Framework ห้ามนำไปตั้งชื่อตัวแปร
reserved = {
    "def": "DEF",  # ใช้สำหรับประกาศฟังก์ชัน
    "return": "RETURN",  # คำสั่งส่งค่ากลับจากฟังก์ชัน
    "get": "GET",  # คำสั่ง HTTP Method GET
    "post": "POST",  # คำสั่ง HTTP Method POST
    "app": "APP",  # ชื่อตัวแปร app (Web Application)
    # ประเภทตัวแปร (Data Types)
    "int": "TYPE_INT",
    "str": "TYPE_STR",
    "float": "TYPE_FLOAT",
    "bool": "TYPE_BOOL",
}

# 1.2 รายชื่อ Token ทั้งหมด (Token List)
# เป็นบัญชีรายชื่อที่ Lexer ต้องรู้จัก ทั้งแบบสัญลักษณ์และคำสงวน
tokens = [
    "ID",  # Identifier: ชื่อตัวแปร หรือชื่อฟังก์ชันที่ผู้ใช้ตั้งเอง
    "NUMBER",  # Number: ตัวเลข (เพิ่มส่วนนี้ที่ขาดหายไป)
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
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COLON = r":"
t_COMMA = r","
t_AT = r"@"
t_DOT = r"\."
t_ignore = " \t"

# 1.4 กฎการตัดคำแบบซับซ้อน (Function Rules)


# กฎสำหรับจัดการ Comment (บรรทัดที่ขึ้นต้นด้วย #)
def t_COMMENT(t):
    r'\#.*'
    pass  # ไม่ return token ใดๆ จะถูกข้ามไป


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


# เพิ่มกฎสำหรับตัวเลข (Number) กลับเข้ามา
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""
    t.value = t.value[1:-1]
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print(f"Lexer Error: เจอตัวอักษรที่ไม่รู้จัก '{t.value[0]}' ที่บรรทัด {t.lexer.lineno}")
    t.lexer.skip(1)


# สร้าง Lexer Object
lexer = lex.lex()
