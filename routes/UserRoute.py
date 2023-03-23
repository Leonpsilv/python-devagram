import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middlewares.JWTMiddleware import token_verify
from models.UserModel import UserCreateModel, UserUpdateModel
from services.AuthService import (
    decode_token_jwt
)
from services.UserService import UserService

router = APIRouter()
userService = UserService()


@router.post("/", response_description="Rota para criar um novo Usuário.")
async def route_create_user(file: UploadFile,user: UserCreateModel = Depends(UserCreateModel)):
    try:
        photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'
        with open(photo_path, 'wb+') as archive:
            archive.write(file.file.read())

        result = await userService.register_user(user, photo_path)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'],
                            detail=result['message'])

        return result

    except Exception as error:
        raise error


@router.get(
    '/me',
    response_description="Rota para buscar as informações do usuário logado.",
    dependencies=[Depends(token_verify)]
)
async def search_for_logged_user_infos(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        result = await userService.search_user(payload['user_id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'],
                                detail=result['message'])
        del result['data']['password']
        return result

    except Exception as error:
        raise error


@router.get(
    '/{user_id}',
    response_description="Rota para buscar as informações do usuário logado.",
    dependencies=[Depends(token_verify)]
)
async def search_for_logged_user_infos(
        user_id: str
):
    try:
        result = await userService.search_user(user_id)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'],
                                detail=result['message'])
        del result['data']['password']
        return result

    except Exception as error:
        raise error


@router.get(
    '/',
    response_description="Rota para todos os usuários.",
    dependencies=[Depends(token_verify)]
)
async def list_all_users(name: str):
    try:
        result = await userService.search_all_users(name)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'],
                                detail=result['message'])
        return result

    except Exception as error:
        raise error


@router.put(
    '/me',
    response_description="Rota para autalizar as informações do usuário logado.",
    dependencies=[Depends(token_verify)]
)
async def update_logged_user_infos(
        Authorization: str = Header(default=''),
        user_update: UserUpdateModel = Depends(UserUpdateModel)
):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        result = await userService.update_logged_user(payload['user_id'], user_update)

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'],
                                detail=result['message'])
        #del result['data']['password']
        return result

    except Exception as error:
        raise error


@router.put(
    "/follow/{followed_user_id}",
    response_description="Rota para dar follow/unfollow em um usuário.",
    dependencies=[Depends(token_verify)]
)
async def follow_unfollow_user(
        followed_user_id: str,
        Authorization: str = Header(default='')
):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await userService.follow_or_unfollow_user(logged_user['id'], followed_user_id)
        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'], detail=result['message'])
        return result
    except Exception as error:
        raise error

