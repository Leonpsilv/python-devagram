
from fastapi import APIRouter, Body, HTTPException

from models.UserModel import UserCreateModel
from services.UserService import (
    register_user
)

router = APIRouter()


@router.post("/", response_description="Rota para criar um novo Usuário.")
async def route_create_user(user: UserCreateModel = Body(...)):
    try:
        result = await register_user(user)

        if not result['status'] == 201:
            raise HTTPException(status_code=result['status'],
                            detail=result['message'])

        return result

    except Exception as error:
        if error.status_code == 400:
            return error

        return {
            'message': 'Erro interno no servidor'
        }
