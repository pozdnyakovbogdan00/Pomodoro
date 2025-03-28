from dataclasses import dataclass
from os.path import exists

from client import GoogleClient
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from repository import UserRepository
from schema import UserLoginShema, UserCreateShema
from jose import jwt, JWTError
from datetime import datetime, timedelta
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        if user := self.user_repository.get_google_user_by_email(email = user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print("user_login")
            return UserLoginShema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateShema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name,
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print("user_create")
        return UserLoginShema(user_id=created_user.id, access_token=access_token)


    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def login(self, username: str, password: str) -> UserLoginShema:
        user = self.user_repository.get_user_by_username(username)
        access_token = self.generate_access_token(user_id=user.id)
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        return UserLoginShema(user_id=user.id, access_token=access_token)

    def generate_access_token(self, user_id: int) -> str:
        expires_date = (datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expires_date},
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ENDCODE_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET, algorithms=[self.settings.JWT_ENDCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        if payload['expire'] < datetime.utcnow().timestamp():
            raise TokenExpired
        return payload['user_id']

