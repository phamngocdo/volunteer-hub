from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    username: str

class UserUpdate(User):
    password: str