from sqlalchemy.orm import Session
from app.models import User
from app.services.auth import verify_password


def get_user(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user(db, username)

    if not user or not verify_password(password, user.password):
        return None
    return user
