# input.py - Test Rebuild
from typing import List, Optional


@app.get("/")
def index():
    return {"message": "HI from dukpyra i am 4 year old"}  # <-- เปลี่ยน message


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0"}  # <-- เพิ่ม version


@app.get("/test")
def test():
    return {"message": "test"}  


@app.get("/test2")
def test():
    return {"message": "test"}
    
@app.get("/test3")
def test():
    return {"message": "test"}  