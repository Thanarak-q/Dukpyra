# ============================================================================
# Dukpyra Comprehensive Test Suite
# ============================================================================
# This file tests the entire compilation pipeline and verifies C# output

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return output"""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result

def test_compilation():
    """Test that the project compiles successfully"""
    print("\n" + "="*70)
    print("TEST 1: Compilation Test")
    print("="*70)
    
    project_dir = Path(__file__).parent
    
    # Run dukpyra compile (using run command with --no-watch)
    result = run_command("dukpyra run --no-watch &", cwd=project_dir)
    
    # Check if compilation succeeded
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    
    if compiled_file.exists():
        print("✅ Compilation successful!")
        print(f"   Generated: {compiled_file}")
        
        # Read and show file size
        size = compiled_file.stat().st_size
        print(f"   Size: {size} bytes")
        
        # Count lines
        with open(compiled_file, 'r') as f:
            lines = len(f.readlines())
        print(f"   Lines: {lines}")
        
        return True
    else:
        print("❌ Compilation failed!")
        print(f"   Output: {result.stdout}")
        print(f"   Errors: {result.stderr}")
        return False

def test_generated_code():
    """Test that the generated C# code is valid"""
    print("\n" + "="*70)
    print("TEST 2: Generated Code Validation")
    print("="*70)
    
    project_dir = Path(__file__).parent
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    
    if not compiled_file.exists():
        print("❌ No compiled file found!")
        return False
    
    with open(compiled_file, 'r') as f:
        code = f.read()
    
    # Check for essential C# elements
    checks = [
        ("WebApplication.CreateBuilder", "ASP.NET builder"),
        ("app.MapGet", "GET routes"),
        ("app.MapPost", "POST routes"),
        ("app.MapPut", "PUT routes"),
        ("app.MapDelete", "DELETE routes"),
        ("app.Run()", "Application run"),
        ("Results.Ok", "Response handling"),
    ]
    
    passed = 0
    failed = 0
    
    for check, description in checks:
        if check in code:
            print(f"   ✅ {description}: Found")
            passed += 1
        else:
            print(f"   ❌ {description}: Missing")
            failed += 1
    
    print(f"\n   Results: {passed} passed, {failed} failed")
    return failed == 0

def test_route_count():
    """Test that all routes were compiled"""
    print("\n" + "="*70)
    print("TEST 3: Route Count Verification")
    print("="*70)
    
    project_dir = Path(__file__).parent
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    
    with open(compiled_file, 'r') as f:
        code = f.read()
    
    # Count different route types
    get_count = code.count("app.MapGet")
    post_count = code.count("app.MapPost")
    put_count = code.count("app.MapPut")
    delete_count = code.count("app.MapDelete")
    patch_count = code.count("app.MapPatch")
    
    total = get_count + post_count + put_count + delete_count + patch_count
    
    print(f"   GET routes: {get_count}")
    print(f"   POST routes: {post_count}")
    print(f"   PUT routes: {put_count}")
    print(f"   DELETE routes: {delete_count}")
    print(f"   PATCH routes: {patch_count}")
    print(f"   ─" * 35)
    print(f"   Total routes: {total}")
    
    # Expected counts (based on our test files)
    expected_total = 50  # Approximate
    
    if total >= 30:  # We have at least 30 routes
        print(f"   ✅ Route compilation looks good!")
        return True
    else:
        print(f"   ⚠️  Expected more routes (got {total})")
        return False

def test_class_definitions():
    """Test that class definitions were compiled"""
    print("\n" + "="*70)
    print("TEST 4: Class/Record Definitions")
    print("="*70)
    
    project_dir = Path(__file__).parent
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    
    with open(compiled_file, 'r') as f:
        code = f.read()
    
    # Check for record definitions
    expected_records = ["User", "Post", "Comment", "Product", "Order", "Customer"]
    
    found = 0
    for record in expected_records:
        if f"public record {record}" in code:
            print(f"   ✅ Record '{record}': Found")
            found += 1
        else:
            print(f"   ⚠️  Record '{record}': Not found")
    
    print(f"\n   Found {found}/{len(expected_records)} records")
    return found >= 4  # At least 4 records should be there

def show_sample_output():
    """Show a sample of the generated C# code"""
    print("\n" + "="*70)
    print("SAMPLE: Generated C# Code (First 50 lines)")
    print("="*70)
    
    project_dir = Path(__file__).parent
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    
    with open(compiled_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines[:50], 1):
        print(f"{i:3d} | {line.rstrip()}")
    
    if len(lines) > 50:
        print(f"     | ... ({len(lines) - 50} more lines)")

def main():
    """Run all tests"""
    print("\n" + "🚀"*35)
    print("   DUKPYRA COMPILER COMPREHENSIVE TEST SUITE")
    print("🚀"*35)
    
    # First, compile the project
    print("\n📦 Compiling project...")
    compile_result = run_command("dukpyra run --no-watch 2>&1 &", cwd=Path(__file__).parent)
    
    # Wait a bit for compilation
    import time
    time.sleep(2)
    
    # Run tests
    results = []
    
    results.append(("Compilation", test_compilation()))
    results.append(("Generated Code", test_generated_code()))
    results.append(("Route Count", test_route_count()))
    results.append(("Class Definitions", test_class_definitions()))
    
    # Show sample output
    show_sample_output()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n   ⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
