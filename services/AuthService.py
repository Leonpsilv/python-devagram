import jwt
from decouple import config
import time

from models.UserModel import UserLoginModel
from repositories.UserRepository import search_user_by_email
from utils.AuthUtil import verify_password

JWT_SECRET = config('JWT_SECRET')


def token_jwt_generate(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token


def decode_token_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if decoded_token['expires'] >= time.time():
            return decoded_token
        else:
            return None

    except Exception as error:
        return



async def login_service(user: UserLoginModel):
    found_user = await search_user_by_email(user.email)
    if not found_user:
        return {
            'message': 'Email ou senha incorretos.',
            'data': '',
            'status': 401
        }
    else:
        if verify_password(user.password, found_user['password']):
            return {
                'message': 'Login realizado com sucesso!',
                'data': found_user,
                'status': 200
            }
        else:
            return {
                'message': 'Email ou senha incorretos.',
                'data': '',
                'status': 401
            }

