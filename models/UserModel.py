from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)

    class Config:
        schema_extra={
            "user": {
                "name": "Jose",
                "email": "jose@email.com",
                "password": "senha123!",
                "photo": "jose.png"
            }
        }


class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)

    class Config:
        schema_extra={
            "user": {
                "name": "Jose",
                "email": "jose@email.com",
                "password": "senha123!",
                "photo": "jose.png"
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "email": "jose@email.com",
                "password": "senha123!",
            }
        }
