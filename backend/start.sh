#!/bin/sh
# Startup script: seed DB (idempotent) then start uvicorn
python scripts/seed_db.py
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
