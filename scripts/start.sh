#!/bin/bash
# EduPredict Full Stack Startup Script

cd "$(dirname "$0")"

echo "========================================"
echo "EduPredict - Academic Intelligence System"
echo "========================================"
echo ""

# Check if PostgreSQL is running
echo "Checking PostgreSQL..."
if ! pg_isready -q; then
    echo "Warning: PostgreSQL is not running. Starting..."
    sudo systemctl start postgresql
    sleep 2
fi

# Start backend in background
echo "Starting Backend..."
cd backend
source venv/bin/activate
export DEBUG=false
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5

# Start frontend
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "EduPredict is now running!"
echo "========================================"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the services, press Ctrl+C"

# Wait for user to stop
wait