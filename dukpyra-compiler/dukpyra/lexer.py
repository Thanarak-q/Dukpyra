import ply.lex as lex

# ==============================================================================
# ส่วนที่ 1: LEXER (ตัวตัดคำ)
# หน้าที่หลัก: เปรียบเสมือน "คนอ่านหนังสือ" ที่จะไล่อ่านโค้ดทีละตัวอักษร
# แล้วจับกลุ่มคำออกมาเป็นชิ้นๆ ที่เรียกว่า "Token" เพื่อส่งต่อให้ Parser
# ==============================================================================

# 1.1 คำสงวน (Reserved Words)
# คือคำที่มีความหมายเฉพาะในภาษา Python หรือ Framework ห้ามนำไปตั้งชื่อตัวแปร
reserved = {
    # Python keywords
    "import": "IMPORT",
    "def": "DEF",
    "class": "CLASS",  # For request body definitions
    "return": "RETURN",
    
    # Boolean and None literals
    "True": "TRUE",
    "False": "FALSE",
    "None": "NONE",
    
    # HTTP Methods
    "get": "GET",
    "post": "POST",
    "put": "PUT",
    "delete": "DELETE",
    "patch": "PATCH",
    
    # Type hints
    "int": "TYPE_INT",
    "str": "TYPE_STR",
    "float": "TYPE_FLOAT",
    "bool": "TYPE_BOOL",
}

# 1.2 รายชื่อ Token ทั้งหมด (Token List)
tokens = [
    "ID",       # Identifier: ชื่อตัวแปร หรือชื่อฟังก์ชันที่ผู้ใช้ตั้งเอง
    "NUMBER",   # Number: ตัวเลข (int หรือ float)
    "STRING",   # String: ข้อความตัวอักษร "" หรือ ''
    "LPAREN",   # (
    "RPAREN",   # )
    "LBRACE",   # {
    "RBRACE",   # }
    "LBRACKET", # [
    "RBRACKET", # ]
    "COLON",    # :
    "COMMA",    # ,
    "AT",       # @
    "DOT",      # .
    "EQUALS",   # =
    "NEWLINE",  # \n
] + list(reserved.values())

# 1.3 กฎการตัดคำแบบง่าย (Simple Regex Rules)
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COLON = r":"
t_COMMA = r","
t_AT = r"@"
t_DOT = r"\."
t_EQUALS = r"="
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


# กฎสำหรับตัวเลข (Number) - รองรับทั้ง int และ float
def t_NUMBER(t):
    r"\d+\.?\d*"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# กฎสำหรับ String - รองรับทั้ง double quotes และ single quotes
def t_STRING(t):
    r'''("[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*')'''
    # ตัดเครื่องหมายคำพูด (ตัวแรกและตัวสุดท้าย) ออก
    t.value = t.value[1:-1]
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print(f"Lexer Error: Unknown character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


# สร้าง Lexer Object
lexer = lex.lex()
