"""
==============================================================================
SETUP.PY - Python Package Configuration
==============================================================================
ไฟล์นี้เป็น configuration สำหรับ build และ distribute Python package

หน้าที่หลัก:
1. กำหนด package metadata (ชื่อ, เวอร์ชัน, author)
2. ระบุ dependencies ที่จำเป็น
3. สร้าง CLI command (dukpyra command)
4. กำหนด Python version ที่รองรับ

การใช้งาน:
    # Development install (แก้โค้ดแล้วใช้งานได้ทันที)
    pip install -e .
    
    # Production install
    pip install .
    
    # Build distribution
    python setup.py sdist bdist_wheel

Setup Tools:
    - find_packages(): หา package ทั้งหมดอัตโนมัติ
    - entry_points: สร้าง CLI command
    - classifiers: ข้อมูล metadata สำหรับ PyPI

หมายเหตุ:
    - ข้อมูล author และ URL ควรอัปเดตเป็นของจริง
    - Version ควรตรงกับ __version__ ใน __init__.py
==============================================================================
"""

from setuptools import setup, find_packages

# อ่าน README สำหรับ long_description (แสดงใน PyPI)
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # ========== Package Identity ==========
    name="dukpyra",                     # ชื่อ package (ใช้ตอน pip install)
    version="0.1.0",                    # เวอร์ชัน (Semantic Versioning)
    author="Your Name",                 # TODO: อัปเดตเป็นชื่อจริง
    author_email="your.email@example.com",  # TODO: อัปเดตเป็น email จริง
    
    # ========== Description ==========
    description="Python to ASP.NET Core Compiler",  # คำอธิบายสั้นๆ
    long_description=long_description,   # คำอธิบายยาว (จาก README.md)
    long_description_content_type="text/markdown",  # รูปแบบของ long_description
    
    # ========== URLs ==========
    url="https://github.com/yourusername/dukpyra",  # TODO: อัปเดต GitHub URL
    
    # ========== Package Discovery ==========
    packages=find_packages(),  # หา packages ทั้งหมดอัตโนมัติ (dukpyra, dukpyra.*)
    
    # ========== Classifiers (Metadata สำหรับ PyPI) ==========
    classifiers=[
        "Development Status :: 3 - Alpha",         # สถานะการพัฒนา (Alpha/Beta/Stable)
        "Intended Audience :: Developers",         # กลุ่มเป้าหมาย
        "License :: OSI Approved :: MIT License",  # License type
        "Programming Language :: Python :: 3",     # ภาษา
        "Programming Language :: Python :: 3.8",   # Python versions ที่รองรับ
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    # ========== Python Version Requirement ==========
    python_requires=">=3.8",  # ต้องใช้ Python 3.8 ขึ้นไป
    
    # ========== Dependencies ==========
    install_requires=[
        "ply>=3.11",         # PLY (Python Lex-Yacc) สำหรับ lexer และ parser
        "watchdog>=3.0.0",   # File watcher สำหรับ hot reload (dukpyra run)
        "click>=8.0.0",      # CLI framework สำหรับ commands
    ],
    
    # ========== CLI Entry Points ==========
    # สร้าง command "dukpyra" ที่เรียก dukpyra.cli:main()
    entry_points={
        "console_scripts": [
            "dukpyra=dukpyra.cli:main",  # $ dukpyra --help
        ],
    },
    
    # ========== Include Extra Files ==========
    include_package_data=True,  # รวมไฟล์ใน MANIFEST.in (templates, ฯลฯ)
)
