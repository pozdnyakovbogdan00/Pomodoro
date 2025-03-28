from pydantic_settings import BaseSettings
from pwd_secret import secret_pwd

class Settings(BaseSettings):
    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5432
    DB_USER: str = 'sa'
    DB_PASSWORD: str = 'pwd'
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET: str = 'secret_key'
    JWT_ENDCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = secret_pwd.GOOGLE_CLIENT_ID
    GOOGLE_SECRET_KEY: str = secret_pwd.GOOGLE_SECRET_KEY
    GOOGLE_REDIRECT_URI: str = secret_pwd.GOOGLE_REDIRECT_URI
    GOOGLE_TOKEN_URL: str = secret_pwd.GOOGLE_TOKEN_URL




    @property
    def db_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"