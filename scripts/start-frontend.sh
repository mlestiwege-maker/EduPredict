#!/bin/bash
# EduPredict Frontend Startup Script

cd "$(dirname "$0")/frontend"

echo "Starting EduPredict Frontend..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start Vite dev server
npm run dev