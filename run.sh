#!/bin/bash
# EduPredict - One Command to Start Everything

set -e

cd "$(dirname "$0")"

echo "========================================"
echo "EduPredict - Academic Intelligence System"
echo "========================================"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check prerequisites
echo "[1/6] Checking prerequisites..."
if ! command_exists python3; then
    echo "ERROR: Python3 is required"
    exit 1
fi
if ! command_exists node; then
    echo "ERROR: Node.js is required"
    exit 1
fi
echo "      ✓ Python3 and Node.js found"

# Step 2: Setup PostgreSQL
echo "[2/6] Setting up PostgreSQL..."
if command_exists docker && docker ps >/dev/null 2>&1; then
    echo "      Starting PostgreSQL via Docker..."
    docker run -d --name edupredict-db \
        -e POSTGRES_DB=edupredict \
        -e POSTGRES_USER=edupredict \
        -e POSTGRES_PASSWORD=edupredict123 \
        -p 5432:5432 \
        postgres:18-alpine 2>/dev/null || true
    sleep 3
    echo "      ✓ PostgreSQL container started"
elif pg_isready -q 2>/dev/null; then
    echo "      ✓ PostgreSQL already running"
else
    echo "      Starting PostgreSQL service..."
    sudo systemctl start postgresql 2>/dev/null || true
    sleep 2
fi

# Step 3: Setup Backend
echo "[3/6] Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "      Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/bin/installed" ]; then
    echo "      Installing Python dependencies..."
    pip install --quiet fastapi uvicorn[standard] sqlalchemy pandas numpy openpyxl python-multipart python-jose passlib python-dotenv pydantic pydantic-settings greenlet asyncpg psycopg2-binary 2>&1 | grep -E "Successfully|error" || true
    touch venv/bin/installed
    echo "      ✓ Dependencies installed"
fi

# Ensure DEBUG is not set to avoid config issues
unset DEBUG

cd ..

# Step 4: Setup Frontend
echo "[4/6] Setting up Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "      Installing npm dependencies..."
    npm install --silent 2>&1 | tail -3
fi
cd ..

# Step 5: Start Services
echo "[5/6] Starting services..."

# Start Backend in background
cd backend
source venv/bin/activate
unset DEBUG
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/edupredict-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "      Waiting for backend..."
for i in {1..15}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo "      ✓ Backend running (PID: $BACKEND_PID)"
        break
    fi
    sleep 1
done

# Start Frontend in background
cd frontend
npm run dev > /tmp/edupredict-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "      Waiting for frontend..."
for i in {1..15}; do
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo "      ✓ Frontend running (PID: $FRONTEND_PID)"
        break
    fi
    sleep 1
done

# Step 6: Complete
echo "[6/6] Complete!"
echo ""
echo "========================================"
echo "EduPredict is now running!"
echo "========================================"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Demo Credentials:"
echo "  Admin: admin@edupredict.com / admin123"
echo "  Lecturer: lecturer@edupredict.com / lecturer123"
echo ""
echo "Logs:"
echo "  Backend:  /tmp/edupredict-backend.log"
echo "  Frontend: /tmp/edupredict-frontend.log"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Keep script running
wait
