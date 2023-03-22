import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile

from middlewares.JWTMiddleware import token_verify
from models.PostModel import CreatePostModel
from services.AuthService import decode_token_jwt
from services.UserService import UserService
from services.PostService import PostService

router = APIRouter()
userService = UserService()
postService = PostService()


@router.post(
    "/",
    response_description="Rota para criar um novo post.",
    dependencies=[Depends(token_verify)]
)
async def route_create_post(Authorization: str = Header(default=''), post: CreatePostModel = Depends(CreatePostModel)):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.register_post(post, logged_user['id'])

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'], detail=result['detail'])
        return result
    except Exception as error:
        raise error


@router.get(
    "/",
    response_description="Rota para listar postagens.",
    dependencies=[Depends(token_verify)]
)
async def route_create_post():
    try:
        result = await postService.list_all_posts()

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])
        return result
    except Exception as error:
        raise error
