from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    user_id: str = Field(...)
    comment: str = Field(...)


class CreateCommentModel(BaseModel):
    comment: str = Field(...)


class EditCommentModel(BaseModel):
    comment: str = Field(...)