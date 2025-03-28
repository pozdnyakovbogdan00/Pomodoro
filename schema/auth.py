from pydantic import BaseModel

class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    access_token: str





