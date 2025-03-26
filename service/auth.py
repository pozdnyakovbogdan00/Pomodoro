from dataclasses import dataclass

from exception import UserNotFoundException, UserNotCorrectPasswordException
from repository import UserRepository
from schema import UserLoginShema


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginShema:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        return UserLoginShema(user_id=user.id, access_token=user.access_token)
