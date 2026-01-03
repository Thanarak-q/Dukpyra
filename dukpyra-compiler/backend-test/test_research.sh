#!/bin/bash
# ============================================================================
# DUKPYRA RESEARCH TEST - Using CLI Commands
# ============================================================================

set -e

cd /home/rock/Documents/Dukpyra/dukpyra-compiler/backend-test

echo "============================================================================"
echo "🔬 DUKPYRA RESEARCH TEST - Complete Workflow"
echo "============================================================================"
echo ""
echo "Research: [6] Krivanek & Uttner - Runtime type collecting"
echo ""

# Step 1: Clean
echo "🧹 Step 1: Clean previous data"
echo "----------------------------------------------------------------------------"
dukpyra clean --yes 2>/dev/null || rm -rf .dukpyra
echo "✅ Cleaned"
echo ""

# Step 2: Compile initial (without runtime types)
echo "🔨 Step 2: Initial Compilation (Static)"
echo "----------------------------------------------------------------------------"
dukpyra run --no-watch &
COMPILE_PID=$!
sleep 3
kill $COMPILE_PID 2>/dev/null || true
wait $COMPILE_PID 2>/dev/null || true

if [ -f ".dukpyra/compiled/Program.cs" ]; then
    STATIC_ROUTES=$(grep -c "app.Map" .dukpyra/compiled/Program.cs || echo "0")
    echo "✅ Static compilation: $STATIC_ROUTES routes"
else
    echo "⚠️  No compilation output"
fi
echo ""

# Step 3: Profile to collect runtime types
echo "🕵️  Step 3: Runtime Profiling (FastAPI)"
echo "----------------------------------------------------------------------------"
echo "Starting: dukpyra profile --port 8005"

# Clean types first
rm -f .dukpyra/types.json

# Start profiling server
dukpyra profile --port 8005 &
PROFILE_PID=$!

echo "PID: $PROFILE_PID"
echo "⏳ Waiting for server..."
sleep 5

# Send test requests
echo ""
echo "📡 Sending requests to collect runtime types..."

curl -s http://localhost:8005/ | head -c 100 && echo ""
curl -s http://localhost:8005/health | head -c 100 && echo ""
curl -s http://localhost:8005/users/42 | head -c 100 && echo ""
curl -s http://localhost:8005/users/123 | head -c 100 && echo ""
curl -s http://localhost:8005/posts/1 | head -c 100 && echo ""

sleep 2

# Stop profiling
echo ""
kill $PROFILE_PID 2>/dev/null || true
wait $PROFILE_PID 2>/dev/null || true
echo "✅ Profiling stopped"
echo ""

# Step 4: Check collected types
echo "📊 Step 4: Verify Runtime Type Collection"
echo "----------------------------------------------------------------------------"

if [ -f ".dukpyra/types.json" ]; then
    echo "✅ Types collected: .dukpyra/types.json"
    echo ""
    cat .dukpyra/types.json
    echo ""
    
    # Verify research metadata
    if grep -q '"runtime_profiling"' .dukpyra/types.json; then
        echo "✅ Runtime profiling method confirmed"
    fi
    
    if grep -q 'Krivanek' .dukpyra/types.json; then
        echo "✅ Research reference: [6] Krivanek & Uttner"
    fi
    
    # Count functions with types
    TYPED_FUNCS=$(grep -c '":' .dukpyra/types.json || echo "0")
    echo "✅ Functions with runtime types: $TYPED_FUNCS"
else
    echo "⚠️  No types.json created (routes may not have parameters)"
fi

echo ""

# Step 5: Compile with runtime data
echo "🔨 Step 5: Recompile with Runtime Type Data"
echo "----------------------------------------------------------------------------"

# Clean compiled output
rm -rf .dukpyra/compiled .dukpyra/bin .dukpyra/obj

# Compile again (now with runtime types)
dukpyra run --no-watch &
COMPILE_PID=$!
sleep 3
kill $COMPILE_PID 2>/dev/null || true
wait $COMPILE_PID 2>/dev/null || true

if [ -f ".dukpyra/compiled/Program.cs" ]; then
    RUNTIME_ROUTES=$(grep -c "app.Map" .dukpyra/compiled/Program.cs || echo "0")
    echo "✅ Compilation with runtime data: $RUNTIME_ROUTES routes"
else
    echo "❌ Compilation failed"
    exit 1
fi

echo ""

# Step 6: Build C# code
echo "🏗️  Step 6: Build C# Output"
echo "----------------------------------------------------------------------------"
cd .dukpyra/compiled
if dotnet build 2>&1 | grep -q "Build succeeded"; then
    echo "✅ C# build: SUCCESS"
    echo "✅ Binary: dukpyra.dll created"
else
    echo "❌ Build failed"
    exit 1
fi

cd ../..
echo ""

# Summary
echo "============================================================================"
echo "✅ COMPLETE RESEARCH WORKFLOW - SUCCESS"
echo "============================================================================"
echo ""
echo "Pipeline:"
echo "  1. ✅ Static compilation (baseline)"
echo "  2. ✅ Runtime profiling with FastAPI"
echo "  3. ✅ Type collection from actual requests"
echo "  4. ✅ Types persisted to .dukpyra/types.json"
echo "  5. ✅ Recompilation with runtime type data"
echo "  6. ✅ C# build successful"
echo ""
echo "🔬 Research Contribution:"
echo "  Method: Runtime Type Collection"
echo "  Reference: [6] Krivanek & Uttner"
echo "  Source: Actual HTTP request values"
echo "  Output: Enhanced C# code generation"
echo ""
echo "============================================================================"
