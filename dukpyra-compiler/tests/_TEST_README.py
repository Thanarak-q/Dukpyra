"""
==============================================================================
TEST FILES - Header Comments Summary
==============================================================================
ไฟล์นี้สรุป header comments สำหรับ test files ทั้งหมด

All test files ใน tests/ directory มีโครงสร้างคล้ายกัน:
    - Import pytest และ modules ที่ต้อง test
    - แบ่ง test cases เป็น classes ตามหมวดหมู่
    - แต่ละ test method ทดสอบ feature เดียว
    - ใช้ assert เพื่อตรวจสอบผลลัพธ์

Test Files:
    1. test_lexer.py      - Lexer tokenization tests
    2. test_parser.py     - Parser และ AST construction tests  
    3. test_analyzer.py   - Semantic analysis tests
    4. test_codegen.py    - C# code generation tests
    5. test_cli.py        - CLI command tests
    6. test_runtime.py    - Runtime type collection tests
    7. test_linq.py       - LINQ transformation tests
    8. test_raw_csharp.py - Raw C# injection tests
    9. test_abstraction.py - Platform abstraction tests

การรัน Tests:
    # รัน tests ทั้งหมด
    pytest tests/ -v
    
    # รัน specific test file
    pytest tests/test_lexer.py -v
    
    # รัน test class
    pytest tests/test_lexer.py::TestLexerKeywords -v
    
    # รัน single test
    pytest tests/test_lexer.py::TestLexerKeywords::test_import_keyword -v
    
    # รันพร้อม coverage report
    pytest tests/ --cov=dukpyra --cov-report=html

Best Practices:
    - แต่ละ test ควรเป็น independent (ไม่พึ่งพา tests อื่น)
    - Test names ควรบอกว่า test อะไร (test_import_keyword)
    - ใช้ assert messages เมื่อ logic ซับซ้อน
    - Group related tests ใน classes

==============================================================================
"""
