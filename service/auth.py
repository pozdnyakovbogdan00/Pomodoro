from dataclasses import dataclass
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpired, TokenNotCorrect
from repository import UserRepository
from schema import UserLoginShema
from jose import jwt, JWTError
from datetime import datetime, timedelta
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

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

