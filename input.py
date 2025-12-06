# input.py - Test Rebuild
from typing import List, Optional


@app.get("/")
def index():
    return {"message": "HI from dukpyra"}  # <-- เปลี่ยน message


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0"}  # <-- เพิ่ม version
