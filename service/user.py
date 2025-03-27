from dataclasses import dataclass
from schema.user import UserLoginShema
from repository import UserRepository
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginShema:
        user = self.user_repository.create_user(username, password)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginShema(user_id=user.id, access_token=access_token)