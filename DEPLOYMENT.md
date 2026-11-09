# EduPredict Deployment Guide

EduPredict is a **split deployment**: frontend on Vercel, backend on a Python-capable platform (Railway/Render/Fly.io/VPS), and PostgreSQL for the database.

## Architecture

```
┌─────────────┐      HTTPS        ┌──────────────┐      HTTPS        ┌─────────────┐
│   User      │──────────────────►│   Vercel     │──────────────────►│   Backend   │
│  (Browser)  │                   │  (Frontend)  │                   │  (FastAPI)  │
└─────────────┘                   └──────────────┘                   └──────┬──────┘
                                                                            │
                                                                ┌───────────▼─────────┐
                                                                │   PostgreSQL        │
                                                                │   (Database)        │
                                                                └─────────────────────┘
```

---

## Part 1: Frontend → Vercel

### Prerequisites
- A [Vercel account](https://vercel.com)
- GitHub repo connected to Vercel

### Steps

1. **Push the code to GitHub** (already done):
   ```bash
   git push origin main
   ```

2. **Import the project in Vercel:**
   - Go to https://vercel.com/dashboard
   - Click **Add New → Project**
   - Import `mlestiwege-maker/EduPredict`
   - Set the **Root Directory** to `frontend`
   - Framework preset: **Vite**
   - Build command: `npm run build`
   - Output directory: `dist`
   - Install command: `npm install`

3. **Add Environment Variables** in Vercel Project Settings:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://your-backend-url.com` (e.g. `https://edupredict-api.railway.app`) |
   | `VITE_APP_NAME` | `EduPredict` |

4. **Deploy:** Click **Deploy**. Vercel builds the frontend and serves it globally.

5. **Note the frontend URL** (e.g. `https://edupredict.vercel.app`) — you'll need it for the backend CORS setting.

---

## Part 2: Backend → Railway (recommended)

Railway has a generous free tier and native Python/PostgreSQL support.

### Steps

1. **Create a Railway project:**
   - Go to https://railway.app
   - Click **New Project → Deploy from GitHub repo**
   - Select `mlestiwege-maker/EduPredict`

2. **Add PostgreSQL database:**
   - In the Railway dashboard, click **New → Database → PostgreSQL**
   - Railway will provision a managed Postgres instance and set `DATABASE_URL` automatically

3. **Deploy the backend service:**
   - Click **New → Service → GitHub repo → EduPredict**
   - Set **Root Directory** to `backend`
   - Railway detects the `Dockerfile` and builds a container
   - Set environment variables from `backend/.env.example`:
     - `DATABASE_URL` (provided by Railway PostgreSQL)
     - `SECRET_KEY` (generate a strong random string)
     - `CORS_ORIGINS` = `https://your-vercel-frontend.vercel.app`
     - `DEBUG=false`

4. **Get the backend URL** (e.g. `https://edupredict-api.railway.app`)

5. **Update Vercel:** Set `VITE_API_URL` to your backend URL and redeploy the frontend.

---

## Part 3: Alternative — Render

1. Go to https://render.com and connect your GitHub repo
2. Create a **Web Service** from the `backend/` directory using the `Dockerfile`
3. Create a **PostgreSQL** database on Render
4. Set env vars from `backend/.env.example`
5. Set `CORS_ORIGINS` to your Vercel frontend URL

---

## Part 4: Alternative — Single VPS (Docker Compose)

For a self-hosted demo, run everything on one VPS:

```bash
# On your VPS
git clone https://github.com/mlestiwege-maker/EduPredict.git
cd EduPredict

# Copy env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit backend/.env: set DATABASE_URL to a managed Postgres or use the docker-compose db service
# Edit frontend/.env: set VITE_API_URL to your VPS domain

# Start all services
docker-compose up -d --build
```

---

## Part 5: Database Setup (Production)

The system uses **PostgreSQL** in production (not SQLite). Run migrations:

```bash
# Backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run Alembic migrations to create tables
alembic upgrade head

# Seed demo users
python scripts/seed_db.py
```

### Demo accounts (created by seed_db.py)
| Role | Email | Password |
|------|-------|----------|
| System Administrator | admin@edupredict.com | admin123 |
| Lecturer | lecturer@edupredict.com | lecturer123 |
| Academic Advisor | advisor@edupredict.com | advisor123 |
| Head of Department | hod@edupredict.com | hod123 |
| Dean | dean@edupredict.com | dean123 |
| Registry Staff | registry@edupredict.com | registry123 |

---

## Part 6: Data (Synthetic Demo)

The system loads synthetic BUSE demo data via:
- `GET /api/v1/data-import/load-demo` (API endpoint)
- Or: `cd backend && python scripts/load_buse_demo.py`

**Important:** This is synthetic demo data for your dissertation — not real BUSE records. For real BUSE deployment, obtain institutional permission and ethics clearance first.

---

## Part 7: ML Models

The ML pipeline trains on-demand via:
- `POST /api/v1/predictions/train/{checkpoint}` (checkpoint: `week_0`, `week_4`, `week_8`, `week_12`)
- `POST /api/v1/predictions/run/{period_id}/{checkpoint}`

Models are saved to `ml/models/` — ensure persistent disk storage on your backend platform.

---

## Checklist Before Deploying

- [ ] `backend/.env` created with production values
- [ ] `frontend/.env` created with `VITE_API_URL` pointing to backend
- [ ] `SECRET_KEY` changed from the default
- [ ] `CORS_ORIGINS` includes your Vercel frontend URL
- [ ] PostgreSQL database provisioned
- [ ] Alembic migrations run (`alembic upgrade head`)
- [ ] Backend reachable over HTTPS
- [ ] Frontend builds successfully on Vercel
- [ ] Report downloads work end-to-end

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Frontend can't reach backend | Check `VITE_API_URL` and backend CORS settings |
| Backend database errors | Ensure `DATABASE_URL` points to a running PostgreSQL |
| ML training fails | Ensure `scikit-learn` and other ML deps are installed (see `requirements.txt`) |
| Report download 404 | Ensure backend has write access to `ml/reports/generated/` |
