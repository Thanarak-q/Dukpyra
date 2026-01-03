"""
==============================================================================
TEST ENHANCED RUNTIME TYPE COLLECTION
==============================================================================
ทดสอบ runtime type collection ที่ปรับปรุงแล้ว
ตามงานวิจัย Krivanek & Uttner [6]
==============================================================================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dukpyra.runtime import DukpyraRuntime

# สร้าง runtime instance
runtime = DukpyraRuntime()

# Custom class สำหรับทดสอบ
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Test 1: Primitive types
print("Test 1: Primitive types")
runtime._collect_type("test_primitives", "num", 42)
runtime._collect_type("test_primitives", "text", "hello")
runtime._collect_type("test_primitives", "flag", True)
runtime._collect_type("test_primitives", "price", 3.14)

# Test 2: List with elements
print("\nTest 2: List types")
runtime._collect_type("test_list", "numbers", [1, 2, 3])
runtime._collect_type("test_list", "names", ["Alice", "Bob"])
runtime._collect_type("test_list", "empty",  [])

# Test 3: Dict
print("\nTest 3: Dict types")
runtime._collect_type("test_dict", "mapping", {"name": "John", "age": 30})
runtime._collect_type("test_dict", "scores", {"math": 90, "english": 85})

# Test 4: Custom classes
print("\nTest 4: Custom class")
user1 = User("Alice", 25)
runtime._collect_type("test_custom", "user", user1)

# Test 5: Nested structures
print("\nTest 5: Nested structures")
users_list = [User("Bob", 30), User("Charlie", 35)]
runtime._collect_type("test_nested", "users", users_list)

# Test 6: Type conflicts
print("\nTest 6: Type conflicts")
runtime._collect_type("test_conflict", "value", 42)      # int
runtime._collect_type("test_conflict", "value", "text")  # str - conflict!

print("\n==============================================================================")
print("Runtime type collection completed!")
print("Check .dukpyra/types.json for results")
print("==============================================================================")

# แสดงผลลัพธ์
import json
types_file = Path(".dukpyra/types.json")
if types_file.exists():
    with open(types_file) as f:
        data = json.load(f)
    
    print("\nFinal Types:")
    print(json.dumps(data.get("types", {}), indent=2, ensure_ascii=False))
    
    print("\nType Observations:")
    print(json.dumps(data.get("observations", {}), indent=2, ensure_ascii=False))
    
    print("\nMetadata:")
    print(json.dumps(data.get("metadata", {}), indent=2, ensure_ascii=False))
