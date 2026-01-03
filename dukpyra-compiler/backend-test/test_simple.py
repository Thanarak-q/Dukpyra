#!/usr/bin/env python3
"""
Simple compilation test - just compile and show results
"""

import sys
import os

# Add parent directory to path so we can import dukpyra
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import subprocess
from pathlib import Path

def main():
    print("="*70)
    print(" DUKPYRA COMPILATION TEST")
    print("="*70)
    
    project_dir = Path(__file__).parent
    print(f"\n📁 Project Directory: {project_dir}")
    
    # List Python files
    py_files = list(project_dir.glob("*.py"))
    py_files = [f for f in py_files if f.name not in ['test_compiler.py', 'test_simple.py']]
    
    print(f"\n📄 Python Files to Compile:")
    for f in py_files:
        size = f.stat().st_size
        print(f"   - {f.name} ({size} bytes)")
    
    print(f"\n🔨 Starting Compilation...")
    print("-"*70)
    
    # Import compiler directly
    try:
        from dukpyra.cli import DukpyraCompiler
        
        compiler = DukpyraCompiler(project_dir)
        compiler.ensure_structure()
        
        success = compiler.compile_project()
        
        print("-"*70)
        
        if success:
            print("\n✅ COMPILATION SUCCESSFUL!")
            
            # Check output
            output_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"
            if output_file.exists():
                size = output_file.stat().st_size
                with open(output_file, 'r') as f:
                    lines = len(f.readlines())
                
                print(f"\n📊 Generated Code Stats:")
                print(f"   File: {output_file.relative_to(project_dir)}")
                print(f"   Size: {size:,} bytes")
                print(f"   Lines: {lines:,}")
                
                # Count routes
                with open(output_file, 'r') as f:
                    content = f.read()
                
                get_count = content.count("app.MapGet")
                post_count = content.count("app.MapPost")
                put_count = content.count("app.MapPut")
                delete_count = content.count("app.MapDelete")
                patch_count = content.count("app.MapPatch")
                record_count = content.count("public record")
                
                print(f"\n🛣️  Route Counts:")
                print(f"   GET:    {get_count}")
                print(f"   POST:   {post_count}")
                print(f"   PUT:    {put_count}")
                print(f"   DELETE: {delete_count}")
                print(f"   PATCH:  {patch_count}")
                print(f"   ─────────────")
                print(f"   TOTAL:  {get_count + post_count + put_count + delete_count + patch_count}")
                
                print(f"\n📦 Data Models:")
                print(f"   Records: {record_count}")
                
                # Show first 30 lines
                print(f"\n📝 Generated C# Code (First 30 lines):")
                print("="*70)
                with open(output_file, 'r') as f:
                    for i, line in enumerate(f, 1):
                        if i > 30:
                            print(f"   ... ({lines - 30} more lines)")
                            break
                        print(f"   {i:3d} | {line.rstrip()}")
                
                return 0
            else:
                print("\n❌ Output file not found!")
                return 1
        else:
            print("\n❌ COMPILATION FAILED!")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
