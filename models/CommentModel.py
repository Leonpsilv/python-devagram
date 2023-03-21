from typing import List

from pydantic import BaseModel, Field

from models import UserModel


class CommentModel(BaseModel):
    user: UserModel = Field(...)
    comment: str = Field(...)