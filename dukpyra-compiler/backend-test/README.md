# Backend Test Project

This is a comprehensive test project for the Dukpyra compiler.

## Test Files

1. **main.py** - Basic CRUD operations
   - Simple GET/POST/PUT/DELETE/PATCH routes
   - Path parameters
   - Multiple path parameters
   - Complex return values

2. **models.py** - Data models and type system
   - Class definitions
   - Typed parameters
   - Mixed parameter types

3. **advanced.py** - Advanced features
   - List comprehensions
   - Dictionary operations
   - Nested data structures
   - Complex expressions

## Test Coverage

### Routes: ~50+ endpoints
- ✅ GET routes (25+)
- ✅ POST routes (8+)
- ✅ PUT routes (4+)
- ✅ DELETE routes (3+)
- ✅ PATCH routes (2+)

### Features Tested
- ✅ Path parameters (`/users/{id}`)
- ✅ Multiple path parameters (`/users/{user_id}/posts/{post_id}`)
- ✅ Class definitions (User, Post, Comment, Product, Order, Customer, Address)
- ✅ Type hints (int, str, float, bool, list, dict)
- ✅ List comprehensions
- ✅ Dictionary literals
- ✅ List literals
- ✅ Nested data structures
- ✅ Boolean values
- ✅ Number operations
- ✅ String operations

## Running Tests

### 1. Compile the project
```bash
cd backend-test
dukpyra run --no-watch
```

### 2. Run automated tests
```bash
python test_compiler.py
```

### 3. View generated C# code
```bash
dukpyra show
```

### 4. Check compilation info
```bash
dukpyra info
```

## Expected Results

- All Python files should compile without errors
- Generated C# code should contain:
  - ASP.NET Core boilerplate
  - All route mappings (MapGet, MapPost, etc.)
  - Record definitions for all classes
  - Proper type conversions
  - LINQ expressions for list comprehensions

## File Structure

```
backend-test/
├── main.py              # Basic routes
├── models.py            # Type system tests
├── advanced.py          # Advanced features
├── test_compiler.py     # Test suite
├── README.md           # This file
└── .dukpyra/           # Compiled output (hidden)
    └── compiled/
        └── Program.cs   # Generated C# code
```

## Success Criteria

✅ Compilation completes without errors
✅ Generated C# file exists
✅ All routes are present in C# code
✅ Class definitions are converted to records
✅ Type hints are properly translated
✅ List comprehensions become LINQ
✅ Dictionaries become C# anonymous objects

## Notes

This test project exercises approximately **2000+ lines of compiler code**:
- Lexer: ~500 lines
- Parser: ~500 lines
- Analyzer: ~370 lines
- CodeGen: ~280 lines
- Runtime: ~540 lines
- CLI: ~590 lines

Total source code tested: **~2780 lines**
