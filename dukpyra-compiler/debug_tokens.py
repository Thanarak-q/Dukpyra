"""
==============================================================================
DEBUG_TOKENS.PY - Lexer Debugging Script
==============================================================================
ไฟล์นี้เป็น utility script สำหรับ debug lexer

หน้าที่:
    - ทดสอบว่า lexer ตัด tokens ถูกต้องหรือไม่
    - แสดงผล tokens ทั้งหมดจากโค้ด input
    - ใช้สำหรับ development และ debugging

การใช้งาน:
    python debug_tokens.py
    
Output ตัวอย่าง:
    LexToken(IMPORT,'import',1,1)
    LexToken(ID,'dukpyra',1,8)
    LexToken(NEWLINE,'\n',1,15)
    LexToken(ID,'app',2,17)
    ...

เมื่อไหร่ใช้:
    - เพิ่ม token type ใหม่ใน lexer
    - แก้ไข regex patterns
    - ตรวจสอบว่า lexer จัดการ edge cases ถูกต้อง
    - Debug lexer errors

หมายเหตุ:
    - แก้ตัวแปร `code` เพื่อทดสอบ input ต่างๆ
    - Tokens จะแสดงตาม format: LexToken(type, value, line, pos)
==============================================================================
"""

from dukpyra.lexer import lexer

# โค้ดตัวอย่างที่ต้องการ debug
code = """
import dukpyra
app = dukpyra.app()

@app.get("/process-numbers")
def process_numbers(numbers: list):
    return [x * 2 for x in numbers]
"""

# ป้อน code เข้า lexer
lexer.input(code)

# วนลูปดึง tokens ทีละตัวและแสดงผล
while True:
    tok = lexer.token()   # ดึง token ถัดไป
    if not tok:           # ถ้าหมด tokens แล้ว
        break
    print(tok)            # แสดง token
