from fastapi import APIRouter, Body, HTTPException

from models.UserModel import UserLoginModel
from services.AuthService import login_service, token_jwt_generate

router = APIRouter()


@router.post('/login')
async def login(user: UserLoginModel = Body(...)):
    result = await login_service(user)

    if not result['status'] == 200:
        raise HTTPException(status_code=result['status'],
                            detail=result['message'])

    del result['data']['password']

    token = token_jwt_generate(result['data']['id'])
    result['data']['token'] = token

    return result
