from sqlalchemy.orm import Session
from sqlalchemy.orm import Query

from API.Database.Models.user import User as ModelUser

from API.Schemas.user import UserPW as SchemaUser

from API.auth import get_password_hash


def get_user(db: Session, user_id: int) -> ModelUser:
    return db.query(ModelUser).filter(ModelUser.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> ModelUser:
    return db.query(ModelUser).filter(ModelUser.username == username).first()


def get_user_by_email(db: Session, email: str) -> ModelUser:
    return db.query(ModelUser).filter(ModelUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> [ModelUser]:
    return db.query(ModelUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: SchemaUser) -> ModelUser:
    db_user = ModelUser(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
