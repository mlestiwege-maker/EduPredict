#!/bin/bash
# EduPredict - One Command to Start Everything

echo "========================================"
echo "EduPredict - Academic Intelligence System"
echo "========================================"
echo ""

# Kill existing processes
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
sleep 1

# Setup backend
cd /home/mufutumari/Desktop/EduPredict/backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -q fastapi uvicorn[standard] sqlalchemy aiosqlite argon2-cffi pandas numpy openpyxl python-multipart passlib python-dotenv pydantic pydantic-settings 2>/dev/null

# Seed database if needed
if [ ! -f "edupredict.db" ]; then
    unset DEBUG
    python scripts/seed_db.py 2>&1 | tail -5
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

# Setup and start frontend
cd /home/mufutumari/Desktop/EduPredict/frontend
[ -d node_modules ] || npm install --silent 2>/dev/null
npm run dev > /tmp/edupredict-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend
for i in {1..10}; do
    curl -s http://localhost:3000 >/dev/null 2>&1 && break
    sleep 1
done

echo ""
echo "========================================"
echo "✅ EduPredict is RUNNING!"
echo "========================================"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Demo Login:"
echo "  Admin:    admin@edupredict.com / admin123"
echo "  Lecturer: lecturer@edupredict.com / lecturer123"
echo "  Advisor:  advisor@edupredict.com / advisor123"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""
wait
