from sqlalchemy.orm import Session
from datetime import date
from app.models.user import User
from app.security.security import get_password_hash

def seed_admin(db: Session) -> None:
    admin = db.query(User).filter(User.login == "admin").first()
    
    if admin:
        return
    
    admin = User(
        login="admin",
        password_hash=get_password_hash("admin"),
        full_name="admin admin",
        birth_date=date(1997, 4, 10),
        city="adminstadt",
        street="adminstrasse",
        postal_code="02137",
        address_email="admin@whatever.com",
        role="admin"
    )
    db.add(admin)
    db.commit()