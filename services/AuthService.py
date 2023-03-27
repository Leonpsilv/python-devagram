import jwt
from decouple import config
import time

from dtos.ResponseDTO import ResponseDTO
from models.UserModel import UserLoginModel
from repositories.UserRepository import UserRepository
from utils.AuthUtil import verify_password

JWT_SECRET = config('JWT_SECRET')
userRepository = UserRepository()


class AuthService:
    def token_jwt_generate(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 6000
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return token

    def decode_token_jwt(self, token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            if decoded_token['expires'] >= time.time():
                return decoded_token
            else:
                return None

        except Exception as error:
            return

    async def login_service(self, user: UserLoginModel):
        found_user = await userRepository.search_user_by_email(user.email)
        if not found_user:
            return ResponseDTO('Email ou senha incorretos.', "", 401)

        else:
            if verify_password(user.password, found_user['password']):
                return ResponseDTO('Login realizado com sucesso!', found_user, 200)

            else:
                return ResponseDTO('Email ou senha incorretos.', '', 401)


