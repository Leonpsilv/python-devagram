from typing import List

from pydantic import BaseModel, Field

from models import CommentModel
from models.UserModel import UserModel


class PostModel(BaseModel):
    id: str = Field(...)
    user: UserModel = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)
    date: str = Field(...)
    likes: str = Field(...)
    comments: List[CommentModel] = Field(...)

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


class CreatePostModel(BaseModel):
    user: UserModel = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)

    class Config:
        schema_extra={
            "postagem": {
                "user": "UserMode",
                "photo": "string",
                "subtitle": "string"
            }
        }