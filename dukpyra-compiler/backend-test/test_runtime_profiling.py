#!/usr/bin/env python3
"""
Test Runtime Type Collection with FastAPI Profiling
"""

import sys
import os
import time
import subprocess
import requests
from pathlib import Path

def test_runtime_profiling():
    """Test that runtime type collection works with FastAPI"""
    
    print("="*70)
    print("🕵️  RUNTIME TYPE COLLECTION TEST (FastAPI Profiling)")
    print("="*70)
    print()
    
    project_dir = Path(__file__).parent
    types_file = project_dir / ".dukpyra" / "types.json"
    
    # Clean types file if exists
    if types_file.exists():
        types_file.unlink()
        print("🧹 Cleaned old types.json")
    
    print("📝 Step 1: Starting FastAPI server for profiling...")
    print("-"*70)
    
    # Start server in background
    server_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "profile_test:app.app", "--port", "8001", "--host", "0.0.0.0"],
        cwd=str(project_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        print("✅ Server started on http://localhost:8001")
        print()
        
        print("📝 Step 2: Sending test requests to collect types...")
        print("-"*70)
        
        # Send test requests
        tests = [
            ("GET", "http://localhost:8001/profile/user/42", "Path param: user_id=42 (int)"),
            ("GET", "http://localhost:8001/profile/user/123", "Path param: user_id=123 (int)"),
            ("GET", "http://localhost:8001/profile/list", "No params"),
            ("POST", "http://localhost:8001/profile/create", "POST request"),
        ]
        
        for method, url, desc in tests:
            try:
                if method == "GET":
                    resp = requests.get(url, timeout=2)
                else:
                    resp = requests.post(url, timeout=2)
                
                if resp.status_code == 200:
                    print(f"   ✅ {desc}: {resp.status_code}")
                else:
                    print(f"   ⚠️  {desc}: {resp.status_code}")
            except Exception as e:
                print(f"   ❌ {desc}: {e}")
        
        print()
        print("📝 Step 3: Checking collected types...")
        print("-"*70)
        
        # Wait a bit for types to be saved
        time.sleep(1)
        
        # Check if types file was created
        if types_file.exists():
            print(f"✅ Types file created: {types_file}")
            
            import json
            with open(types_file, 'r') as f:
                types_data = json.load(f)
            
            print()
            print("📊 Collected Type Data:")
            print(json.dumps(types_data, indent=2))
            print()
            
            # Verify data structure
            if "types" in types_data:
                print("✅ Types section found")
                
                if "get_user" in types_data["types"]:
                    user_types = types_data["types"]["get_user"]
                    print(f"✅ get_user types: {user_types}")
                    
                    if "user_id" in user_types:
                        if user_types["user_id"] == "int":
                            print("✅ user_id type correctly inferred as 'int'")
                        else:
                            print(f"⚠️  user_id type is '{user_types['user_id']}', expected 'int'")
            
            if "observations" in types_data:
                print("✅ Observations section found")
            
            if "metadata" in types_data:
                metadata = types_data["metadata"]
                print(f"✅ Metadata: version={metadata.get('version')}, method={metadata.get('method')}")
            
            print()
            return True
        else:
            print(f"❌ Types file not created at {types_file}")
            return False
            
    finally:
        # Stop server
        print()
        print("🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped")

def main():
    print()
    print("🚀 Testing Dukpyra Runtime Type Collection")
    print()
    
    # Check dependencies
    try:
        import uvicorn
        import fastapi
        import requests
        print("✅ Dependencies installed (FastAPI, Uvicorn, Requests)")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print()
        print("Install with: pip install fastapi uvicorn requests")
        return 1
    
    print()
    
    # Run test
    success = test_runtime_profiling()
    
    print()
    print("="*70)
    if success:
        print("✅ RUNTIME TYPE COLLECTION TEST: PASSED")
    else:
        print("❌ RUNTIME TYPE COLLECTION TEST: FAILED")
    print("="*70)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
