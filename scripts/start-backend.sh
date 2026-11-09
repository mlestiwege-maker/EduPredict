#!/bin/bash
# EduPredict Backend Startup Script

cd "$(dirname "$0")/backend"

echo "Starting EduPredict Backend..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export DEBUG=false

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload