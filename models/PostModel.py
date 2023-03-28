from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field

from models.UserModel import UserModel
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class PostModel(BaseModel):
    id: str = Field(...)
    user_id: str = Field(...)
    photo: str = Field(...)
    subtitle: str = Field(...)
    date: str
    likes: List
    comments: List
    user: Optional[UserModel]
    total_likes: int
    total_comments: int

    def __getitem__(self, item):
        return getattr(self, item)

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
