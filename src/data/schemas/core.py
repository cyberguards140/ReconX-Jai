from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "viewer"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
