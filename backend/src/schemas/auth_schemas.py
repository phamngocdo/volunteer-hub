from pydantic import BaseModel, EmailStr

class AuthUser(BaseModel):
    email: EmailStr
    password: str

class AuthLogin(AuthUser):
    pass

class AuthRegister(AuthUser):
    username: str
    phone: str