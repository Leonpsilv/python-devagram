from models.UserModel import UserCreateModel
from repositories.UserRepository import (
    create_user,
    list_users,
    search_user_by_email,
    search_user_by_id,
    edit_user,
    delete_user
)


async def register_user (user: UserCreateModel):
    try:
        found_user = await search_user_by_email(user.email)
        if found_user:
            return {
                "message" : "Este email já está cadastrado!",
                "data" : "",
                "status" : 400
            }
        else:
            new_user = await create_user(user)
            return {
                "message" : "Usuário cadastrado com sucesso!",
                "data" : new_user,
                "status": 201
            }
    except Exception as error:
        return {
            "message" : "Erro interno no servidor",
            "data" : str(error),
            "status" : 500
        }

async def search_user(id: str):
    try:
        found_user = await search_user_by_id(id)
        if found_user:
            return {
                "message" : "Login realizado com sucesso",
                "data" : found_user,
                "status": 200
            }
        else:
            return {
                "message" : "Usuário (com esse id) não encontrado",
                "data" : "",
                "status": 404
            }

    except Exception as error:
        return {
            "message" : "Erro interno no servidor",
            "data" : str(error),
            "status" : 500
        }