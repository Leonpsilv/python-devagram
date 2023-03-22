from fastapi import Form, UploadFile
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


def form_body(cls): #decorator para multipart/form-data
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra={
            "user": {
                "name": "Jose",
                "email": "jose@email.com",
                "password": "senha123!"
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

@form_body
class UserUpdateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: UploadFile = Field(...)

    class Config:
        schema_extra={
            "user": {
                "name": "Jose",
                "email": "jose@email.com",
                "password": "senha123!"
            }
        }
