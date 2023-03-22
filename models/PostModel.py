from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, Field

from models.UserModel import UserModel
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class PostModel(BaseModel):
    id: str = Field(...)
    user: UserModel = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)
    date: str = Field(...)
    likes: str = Field(...)
    comments: List = Field(...)

    class Config:
        schema_extra={
            "postagem": {
                "id": "string",
                "user": "",
                "photo": "string",
                "subtitle": "string",
                "date": "date",
                "likes": "int",
                "comments": "List[comments]"
            }
        }

@decoratorUtil.form_body
class CreatePostModel(BaseModel):
    photo: UploadFile = Field(...)
    subtitle: str = Field(...)

    class Config:
        schema_extra={
            "postagem": {
                "photo": "string",
                "subtitle": "string"
            }
        }
