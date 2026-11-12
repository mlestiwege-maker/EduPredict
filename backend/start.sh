#!/bin/sh
# Startup script: seed DB (idempotent), load institutional dataset, then start uvicorn
python scripts/seed_db.py
python scripts/load_buse_demo.py
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
