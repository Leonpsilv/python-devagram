from typing import List

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class UserModel(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    photo: str = Field(...)
    followers: List
    following: List
    total_followers: int
    total_following: int
    all_posts: List
    total_posts: int
    token: str

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra={
            "user": {
                "name": "string",
                "email": "string",
                "password": "string",
                "photo": "string",
                "followers": "List",
                "following": "List"
            }
        }


@decoratorUtil.form_body
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

@decoratorUtil.form_body
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
