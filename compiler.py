import ast

from jinja2 import Template

# Config
INPUT_FILE = "input.py"
OUTPUT_FILE = "services/Program.cs"

# ==============================================
# 📄 C# Template (Embedded)
# ==============================================
CSHARP_TEMPLATE = """
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// --- Dukpyra Generated Routes ---
{% for route in routes %}
app.Map{{ route.method }}("{{ route.path }}", ({{ route.params }}) =>
{
    return Results.Ok({{ route.return_data }});
});
{% endfor %}
// --------------------------------

app.Run();
""".strip()

# ==============================================
# 🗺️ Type Mapping: Python → C#
# ==============================================
TYPE_MAP = {
    "str": "string",
    "int": "int",
    "float": "double",
    "bool": "bool",
    "bytes": "byte[]",
    "None": "void",
    "Any": "object",
    # Datetime
    "datetime": "DateTime",
    "date": "DateOnly",
    "time": "TimeOnly",
}


def convert_type_hint(node) -> str:
    """
    แปลง AST node ของ type hint ไปเป็น C# type string
    รองรับ:
      - Basic types: str, int, float, bool
      - List[X] → List<X>
      - Optional[X] → X?
      - Dict[K, V] → Dictionary<K, V>
      - Union[X, Y] → object (simplified)
    """
    if node is None:
        return "string"  # default ถ้าไม่มี type hint

    # 1. Basic types (ast.Name) เช่น `str`, `int`
    if isinstance(node, ast.Name):
        py_type = node.id
        return TYPE_MAP.get(py_type, py_type)  # ถ้าไม่รู้จักก็ใช้ชื่อเดิม (อาจเป็น custom class)

    # 2. Constant None
    if isinstance(node, ast.Constant) and node.value is None:
        return "void"

    # 3. Subscript types (Generic) เช่น `List[str]`, `Optional[int]`
    if isinstance(node, ast.Subscript):
        # ดึงชื่อ Generic type (List, Optional, Dict, etc.)
        if isinstance(node.value, ast.Name):
            generic_name = node.value.id
        elif isinstance(node.value, ast.Attribute):
            # typing.List → ดึง 'List'
            generic_name = node.value.attr
        else:
            return "object"

        # ดึง arguments ใน [] 
        # Python 3.9+: node.slice เป็น node ตรงๆ
        # Python 3.8: node.slice เป็น ast.Index
        slice_node = node.slice
        if isinstance(slice_node, ast.Index):  # Python 3.8 compatibility
            slice_node = slice_node.value

        # --- Handle แต่ละ Generic Type ---
        
        # List[X] → List<X>
        if generic_name in ("List", "list"):
            inner_type = convert_type_hint(slice_node)
            return f"List<{inner_type}>"

        # Optional[X] → X? (nullable)
        if generic_name == "Optional":
            inner_type = convert_type_hint(slice_node)
            return f"{inner_type}?"

        # Dict[K, V] → Dictionary<K, V>
        if generic_name in ("Dict", "dict"):
            if isinstance(slice_node, ast.Tuple) and len(slice_node.elts) == 2:
                key_type = convert_type_hint(slice_node.elts[0])
                val_type = convert_type_hint(slice_node.elts[1])
                return f"Dictionary<{key_type}, {val_type}>"
            return "Dictionary<string, object>"

        # Set[X] → HashSet<X>
        if generic_name in ("Set", "set"):
            inner_type = convert_type_hint(slice_node)
            return f"HashSet<{inner_type}>"

        # Tuple[X, Y, ...] → (X, Y, ...) C# ValueTuple
        if generic_name in ("Tuple", "tuple"):
            if isinstance(slice_node, ast.Tuple):
                inner_types = [convert_type_hint(el) for el in slice_node.elts]
                return f"({', '.join(inner_types)})"
            return f"({convert_type_hint(slice_node)},)"

        # Union[X, Y] → object (simplified, C# ไม่มี Union ตรงๆ)
        if generic_name == "Union":
            # ถ้าเป็น Union[X, None] = Optional[X]
            if isinstance(slice_node, ast.Tuple):
                non_none = [el for el in slice_node.elts 
                           if not (isinstance(el, ast.Constant) and el.value is None)]
                if len(non_none) == 1:
                    return f"{convert_type_hint(non_none[0])}?"
            return "object"

        # Generic อื่นๆ ที่ไม่รู้จัก
        return "object"

    # 4. Attribute access เช่น `typing.List`
    if isinstance(node, ast.Attribute):
        return TYPE_MAP.get(node.attr, node.attr)

    # 5. BinOp สำหรับ Python 3.10+ union syntax: X | Y
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        # ถ้าฝั่งใดฝั่งหนึ่งเป็น None → nullable
        left = node.left
        right = node.right
        if isinstance(right, ast.Constant) and right.value is None:
            return f"{convert_type_hint(left)}?"
        if isinstance(left, ast.Constant) and left.value is None:
            return f"{convert_type_hint(right)}?"
        return "object"

    # Fallback
    return "object"


# Helper Function: แกะค่าจาก Dict ของ Python -> C# Anonymous Object
def parse_return_dict(dict_node):
    """
    แปลง {'status': 'ok'} (Python)
    เป็น new { status = "ok" } (C#)
    """
    pairs = []
    # zip คือการจับคู่ key กับ value ใน dict
    for key, value in zip(dict_node.keys, dict_node.values):
        # 1. จัดการ Key (C# property ไม่ต้องมี quotes)
        if isinstance(key, ast.Constant):  # Python 3.8+ ใช้ Constant
            k_str = key.value
        elif isinstance(key, ast.Str):  # Python เก่า
            k_str = key.s
        else:
            k_str = "unknown_key"

        # 2. จัดการ Value
        if isinstance(value, ast.Constant):
            val = value.value
            if isinstance(val, str):
                v_str = f'"{val}"'  # ใส่ quotes ถ้าเป็น string
            elif isinstance(val, bool):
                v_str = str(val).lower()  # True -> true
            else:
                v_str = str(val)  # int, float
        else:
            v_str = "null"  # กรณีซับซ้อนอื่นๆ ขอข้ามไปก่อน

        pairs.append(f"{k_str} = {v_str}")

    return "new { " + ", ".join(pairs) + " }"


def dukpyra_compile():
    print(f"📂 Reading source: {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    routes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # ... (ส่วนแกะ Route/Params เหมือนเดิม) ...
            method = "Get"
            path = "/"
            if node.decorator_list:
                deco = node.decorator_list[0]
                # Handle @app.get("/path") syntax
                if isinstance(deco, ast.Attribute):
                    # This is for @app.get (without parentheses)
                    method = deco.attr.capitalize()
                    path = "/"  # default path
                elif isinstance(deco, ast.Call):
                    # This is for @app.get("/path")
                    if isinstance(deco.func, ast.Attribute):
                        method = deco.func.attr.capitalize()
                        if deco.args:
                            path = deco.args[0].value

            csharp_params = []
            for arg in node.args.args:
                py_name = arg.arg
                # 🔥 ใช้ Type Mapping แทน hardcode!
                csharp_type = convert_type_hint(arg.annotation)
                csharp_params.append(f"{csharp_type} {py_name}")

            # --- 🔥 ส่วนใหม่: เจาะหา Return Value ---
            csharp_return = 'new { message = "No content" }'  # ค่า default

            for stmt in node.body:
                # เช็คว่าเจอบรรทัด return ไหม?
                if isinstance(stmt, ast.Return):
                    # เช็คว่าสิ่งที่ return เป็น Dict ({...}) หรือไม่?
                    if isinstance(stmt.value, ast.Dict):
                        csharp_return = parse_return_dict(stmt.value)
                    break

            routes.append(
                {
                    "method": method,
                    "path": path,
                    "function_name": node.name,
                    "params": ", ".join(csharp_params),
                    "return_data": csharp_return,  # <--- ส่ง data ตัวจริงไป!
                }
            )

    print("⚙️  Rendering C# code...")
    template = Template(CSHARP_TEMPLATE)
    csharp_code = template.render(routes=routes)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(csharp_code)

    print(f"✅ Generated with ACTUAL returns!")


if __name__ == "__main__":
    dukpyra_compile()
