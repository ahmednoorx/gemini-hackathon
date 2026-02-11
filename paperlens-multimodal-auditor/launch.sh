#!/bin/bash
# Launch script for PaperLens (fixes Streamlit upload issues in Codespaces)

echo "🚀 Starting PaperLens..."
echo ""

# Activate virtual environment
cd /workspaces/gemini-hackathon/paperlens-multimodal-auditor
source .venv/bin/activate

# Start backend
echo "📦 Starting backend on http://localhost:8000..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend with XSRF/CORS disabled (fixes 403 upload errors)
echo "🎨 Starting frontend on http://localhost:8501..."
cd ../frontend
python -m streamlit run app.py \
  --server.port 8501 \
  --server.address 127.0.0.1 \
  --server.enableXsrfProtection false \
  --server.enableCORS false \
  --server.maxUploadSize 1024 &
FRONTEND_PID=$!

echo ""
echo "✅ PaperLens is running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for user to stop
wait
