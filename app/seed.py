from app.db.seed import seed_admin
from app.db.session import SessionLocal

def run():
    db = SessionLocal()
    try:
        seed_admin(db)
        print("✅ Admin seeded")
    finally:
        db.close()

if __name__ == "__main__":
    run()