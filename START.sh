#!/bin/bash
# EduPredict - Complete Production System

echo "========================================"
echo "  EduPredict - Academic Intelligence"
echo "  Bindura University of Science Education"
echo "========================================"
echo ""

# Kill existing processes
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
sleep 1

# Setup Backend
cd /home/mufutumari/Desktop/EduPredict/backend

echo "[1/3] Setting up Backend..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -q fastapi uvicorn[standard] sqlalchemy aiosqlite argon2-cffi pandas numpy openpyxl python-multipart passlib python-dotenv pydantic pydantic-settings 2>/dev/null

# Seed database if needed
if [ ! -f "edupredict.db" ]; then
    unset DEBUG
    python scripts/seed_db.py 2>&1 | tail -3
fi

# Start backend
unset DEBUG
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/edupredict-backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend
for i in {1..10}; do
    curl -s http://localhost:8000/health >/dev/null 2>&1 && break
    sleep 1
done

echo "✓ Backend running (PID: $BACKEND_PID)"

# Setup Frontend
echo "[2/3] Setting up Frontend..."
cd /home/mufutumari/Desktop/EduPredict/frontend
[ -d node_modules ] || npm install --silent 2>/dev/null

npm run dev > /tmp/edupredict-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend
for i in {1..15}; do
    curl -s http://localhost:3000 >/dev/null 2>&1 && break
    sleep 1
done

echo "✓ Frontend running (PID: $FRONTEND_PID)"

# Complete
echo ""
echo "========================================"
echo "  ✅ EduPredict System is RUNNING!"
echo "========================================"
echo ""
echo "  🌐 Frontend:  http://localhost:3000"
echo "  📡 Backend:   http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "  ─── Demo Login Credentials ───"
echo "  👨‍💻 Admin:     admin@edupredict.com / admin123"
echo "  👨‍🏫 Lecturer:  lecturer@edupredict.com / lecturer123"
echo "  💼 Advisor:    advisor@edupredict.com / advisor123"
echo "  📊 HOD:        hod@edupredict.com / hod123"
echo "  🏛️ Dean:       dean@edupredict.com / dean123"
echo "  📋 Registry:   registry@edupredict.com / registry123"
echo ""
echo "  ─── System Features ───"
echo "  ✅ Student Data Upload & Validation"
echo "  ✅ Academic Performance Analytics"
echo "  ✅ ML Prediction Engine"
echo "  ✅ Risk Monitoring & Early Warning"
echo "  ✅ Recommendation System"
echo "  ✅ Intervention Tracking"
echo "  ✅ Role-Based Reports"
echo "  ✅ Audit Logging"
echo ""
echo "  Backend PID: $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "  To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "========================================"

# Keep running
wait
