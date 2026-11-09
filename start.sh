#!/bin/bash
echo "========================================"
echo "EduPredict - Academic Intelligence System"
echo "========================================"
echo ""

# Start PostgreSQL if needed
if ! pg_isready -q 2>/dev/null; then
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql 2>/dev/null || true
    sleep 2
fi

# Start Backend
echo "Starting Backend..."
cd /home/mufutumari/Desktop/EduPredict/backend
source venv/bin/activate 2>/dev/null || { python3 -m venv venv && source venv/bin/activate; }
pip install -q fastapi uvicorn sqlalchemy pandas numpy openpyxl python-multipart passlib python-dotenv pydantic pydantic-settings greenlet asyncpg psycopg2-binary 2>/dev/null
unset DEBUG
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/edupredict-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend
echo "Waiting for backend..."
for i in {1..10}; do
    curl -s http://localhost:8000/health >/dev/null 2>&1 && break
    sleep 1
done

# Start Frontend
echo "Starting Frontend..."
cd /home/mufutumari/Desktop/EduPredict/frontend
[ -d node_modules ] || npm install --silent 2>/dev/null
npm run dev > /tmp/edupredict-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "EduPredict is RUNNING!"
echo "========================================"
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Demo Login:"
echo "  Admin: admin@edupredict.com / admin123"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""
wait
