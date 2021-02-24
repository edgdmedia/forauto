from pydantic import BaseModel, EmailStr


class UserInput(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    address: str
    phone_number: str
    city: str
    state: str
    password: bytes
    confirm_password: bytes
    website_url: str


class UpdateUserInput(BaseModel):
    userId: str


class GetPasswordResetLink(BaseModel):
    email: EmailStr
    website_url: str


class PasswordResetInput(BaseModel):
    userId: str
    password: bytes
    confirm_password: bytes


class UserLoginInput(BaseModel):
    email: EmailStr
    password: bytes
