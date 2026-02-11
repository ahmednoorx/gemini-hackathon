#!/bin/bash

# PaperLens Health Check
# Validates that the system is properly set up

echo "🔍 PaperLens Health Check"
echo "=========================="
echo ""

# 1. Check Python
echo "1️⃣ Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found"
    exit 1
fi

# 2. Check .env file
echo ""
echo "2️⃣ Checking backend configuration..."
if [ -f "backend/.env" ]; then
    if grep -q "GOOGLE_API_KEY=" backend/.env; then
        KEY=$(grep "GOOGLE_API_KEY=" backend/.env | cut -d= -f2)
        if [ -z "$KEY" ] || [ "$KEY" == "your_api_key_here" ]; then
            echo "   ⚠️  API key not set (found placeholder)"
        else
            echo "   ✅ GOOGLE_API_KEY is configured"
        fi
    else
        echo "   ⚠️  GOOGLE_API_KEY not found in .env"
    fi
else
    echo "   ❌ backend/.env not found"
    echo "   Run: cp backend/.env.example backend/.env"
    exit 1
fi

# 3. Check backend requirements
echo ""
echo "3️⃣ Checking backend dependencies..."
if python3 -c "import fastapi, google.genai, pymupdf" 2>/dev/null; then
    echo "   ✅ All backend packages found"
else
    echo "   ❌ Missing backend packages"
    echo "   Run: pip install -r backend/requirements.txt"
    exit 1
fi

# 4. Check frontend requirements
echo ""
echo "4️⃣ Checking frontend dependencies..."
if python3 -c "import streamlit, requests" 2>/dev/null; then
    echo "   ✅ All frontend packages found"
else
    echo "   ❌ Missing frontend packages"
    echo "   Run: pip install -r frontend/requirements.txt"
    exit 1
fi

# 5. Check key files exist
echo ""
echo "5️⃣ Checking project structure..."
FILES_TO_CHECK=(
    "backend/main.py"
    "backend/gemini_auditor.py"
    "backend/ingestion.py"
    "frontend/app.py"
    ".streamlit/config.toml"
)

ALL_EXIST=true
for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        ALL_EXIST=false
    fi
done

# Final status
echo ""
echo "=========================="
if [ "$ALL_EXIST" = true ]; then
    echo "✅ System is ready to run!"
    echo ""
    echo "Next steps:"
    echo "  Terminal 1: cd backend && python main.py"
    echo "  Terminal 2: cd frontend && streamlit run app.py --server.address 0.0.0.0"
    echo ""
    echo "Then open: http://localhost:8501"
else
    echo "⚠️  Please fix the above issues before running."
fi
echo ""
