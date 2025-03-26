import string
from dataclasses import dataclass
from random import random, choice

from schema.user import UserLoginShema
from repository import UserRepository

@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginShema:
        user = self.user_repository.create_user(username, password, self._generate_access_token())
        return UserLoginShema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return "".join(choice(string.ascii_uppercase + string.digits) for _ in range (10))