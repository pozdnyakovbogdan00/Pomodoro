from dataclasses import dataclass

from sqlalchemy.orm import Session
from models.user import UserProfile
from sqlalchemy import insert, select

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, username: str, password: str) -> UserProfile | None:
        query = insert(UserProfile).values(
            username=username,
            password=password).returning(UserProfile.id)
        with (self.db_session() as session):
            user_id: str = session.execute(query).scalar()
            session.commit()
            return self.get_user(user_id)

    def get_user(self, user_id: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()