#!/bin/bash

# PaperLens Quick Start Script
# Scaffolds and runs the entire system

set -e

echo "🚀 PaperLens Quick Start"
echo "========================"

# Step 1: Environment Setup
echo ""
echo "📦 Step 1: Setting up environment..."

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created .env file. Please edit it with your GOOGLE_API_KEY"
    echo "   You can get an API key from: https://aistudio.google.com/app/apikey"
else
    echo "✅ .env file already exists"
fi

# Step 2: Install Backend Dependencies
echo ""
echo "📚 Step 2: Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..
echo "✅ Backend dependencies installed"

# Step 3: Install Frontend Dependencies
echo ""
echo "🎨 Step 3: Installing frontend dependencies..."
cd frontend
pip install -r requirements.txt
cd ..
echo "✅ Frontend dependencies installed"

# Step 4: Instructions
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Edit backend/.env and add your GOOGLE_API_KEY"
echo ""
echo "2. Start the backend server:"
echo "   cd backend && python main.py"
echo ""
echo "3. In a new terminal, start the Streamlit frontend:"
echo "   cd frontend && streamlit run app.py"
echo ""
echo "4. Open your browser to:"
echo "   - Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:8501"
echo ""
echo "5. Upload a PDF and watch PaperLens detect contradictions! 🎉"
echo ""
echo "📖 Documentation:"
echo "   - Architecture: docs/architecture.md"
echo "   - Gemini 3 API: docs/gemini3_api_guide.md"
echo "   - Demo Script: docs/demo_script.md"
echo "   - Devpost: docs/devpost_submission.md"
echo ""
echo "Questions? Check the README.md for more details."
