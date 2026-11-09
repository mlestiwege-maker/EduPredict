"""Seed the database with initial data including demo users (portable)."""
import sys
from pathlib import Path
# allow running from repo root or backend/
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base, User, Role
from app.core.security import hash_password

ROLES = [
    {"name": "system_admin", "description": "System Administrator"},
    {"name": "lecturer", "description": "Lecturer"},
    {"name": "academic_advisor", "description": "Academic Advisor"},
    {"name": "head_of_department", "description": "Head of Department"},
    {"name": "dean", "description": "Dean"},
    {"name": "registry", "description": "Registry Staff"},
]
USERS = [
    {"email": "admin@edupredict.com", "password": "admin123", "full_name": "System Administrator", "role_name": "system_admin"},
    {"email": "lecturer@edupredict.com", "password": "lecturer123", "full_name": "Dr. Sarah Johnson (Lecturer)", "role_name": "lecturer"},
    {"email": "advisor@edupredict.com", "password": "advisor123", "full_name": "Michael Chen (Academic Advisor)", "role_name": "academic_advisor"},
    {"email": "hod@edupredict.com", "password": "hod123", "full_name": "Prof. Emily Williams (HOD)", "role_name": "head_of_department"},
    {"email": "dean@edupredict.com", "password": "dean123", "full_name": "Dr. Robert Davis (Dean)", "role_name": "dean"},
    {"email": "registry@edupredict.com", "password": "registry123", "full_name": "Grace Moyo (Registry)", "role_name": "registry"},
]

def seed_database():
    # sync URL for seeding
    url = settings.database_url
    if url.startswith("sqlite+aiosqlite"):
        url = url.replace("sqlite+aiosqlite", "sqlite")
    engine = create_engine(url, echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        if session.query(User).count() > 0:
            print("Users already exist; ensuring roles present.")
        roles = {}
        for r in ROLES:
            role = session.query(Role).filter_by(name=r["name"]).first()
            if not role:
                role = Role(**r, is_active=True); session.add(role); session.flush()
            roles[r["name"]] = role
        for u in USERS:
            if session.query(User).filter_by(email=u["email"]).first():
                continue
            session.add(User(email=u["email"], hashed_password=hash_password(u["password"]), full_name=u["full_name"], role_id=roles[u["role_name"]].id, is_active=True, is_verified=True))
        session.commit()
        print("Seed complete. Demo accounts:")
        for u in USERS:
            print(f"  {u['role_name']}: {u['email']} / {u['password']}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
