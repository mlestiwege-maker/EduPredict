#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "EduPredict — Academic Performance Prediction System"
echo "=================================================="

# Kill any existing processes on ports 8000 and 3000
echo "Stopping any existing EduPredict processes..."
pkill -f 'uvicorn app.main:app' 2>/dev/null || true
pkill -f 'vite' 2>/dev/null || true
sleep 1

# Load synthetic demo data
echo "Loading synthetic BUSE demo dataset..."
cd "$ROOT/backend"
./venv/bin/python scripts/load_buse_demo.py >/tmp/edupredict-seed.log 2>&1 || echo "Seed load skipped (may already be loaded)"

# Start backend
echo "Starting backend on http://127.0.0.1:8000 ..."
cd "$ROOT/backend"
setsid ./venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir "$ROOT/backend" >/tmp/edupredict-api.log 2>&1 < /dev/null &

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in $(seq 1 30); do
  if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "Backend is ready."
    break
  fi
  sleep 1
done

# Start frontend
echo "Starting frontend on http://127.0.0.1:3000 ..."
cd "$ROOT/frontend"
exec npm run dev -- --host 127.0.0.1 --port 3000
