from fastapi import Header, HTTPException

from services.AuthService import AuthService
authService = AuthService()


async def token_verify(Authorization: str = Header(default='')):
    if not Authorization.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail="Necessário token para autenticação.")

    token = Authorization.split(' ')[1]

    payload = authService.decode_token_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    return payload
