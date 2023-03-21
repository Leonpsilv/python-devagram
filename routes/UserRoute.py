import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middlewares.JWTMiddleware import token_verify
from models.UserModel import UserCreateModel
from services.AuthService import (
    decode_token_jwt
)
from services.UserService import (
    register_user,
    search_user
)

router = APIRouter()


@router.post("/", response_description="Rota para criar um novo Usuário.")
async def route_create_user(file: UploadFile,user: UserCreateModel = Depends(UserCreateModel)):
    try:
        photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'
        with open(photo_path, 'wb+') as archive:
            archive.write(file.file.read())

        result = await register_user(user, photo_path)

        os.remove(photo_path)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'],
                            detail=result['message'])

        return result

    except Exception as error:
        print(error)
        if error.status_code == 400:
            raise HTTPException(status_code=error.status_code,
                                detail=error.detail)
        detail = {
            'detail': 'Erro interno no servidor'
        }
        raise HTTPException(status_code=500,
                            detail=detail)

@router.get(
    '/me',
    response_description="Rota para buscar as informações do usuário logado.",
    dependencies=[Depends(token_verify)]
)
async def search_for_logged_user_infos(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        result = await search_user(payload['user_id'])

        if not result['status'] == 200:
            raise HTTPException(status_code=result['status'],
                                detail=result['message'])
        del result['data']['password']
        return result
    except Exception as error:
        raise HTTPException(status_code=error.status_code,
                            detail=error.detail)