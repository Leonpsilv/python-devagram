from models.UserModel import UserCreateModel
from repositories.UserRepository import (
    create_user,
    list_users,
    search_user_by_email,
    edit_user,
    delete_user
)

async def register_user (user: UserCreateModel):
    try:
        user_found = await search_user_by_email(user.email)
        if user_found:
            return {
                "message" : "Este email ja esta cadastrado",
                "data" : "",
                "status" : 400
            }
        else:
            new_user = await create_user(user)
            return {
                "message" : "Usuario cadastrado com sucesso",
                "data" : new_user,
                "status": 201
            }
    except Exception as error:
        return {
            "message" : "Erro interno no servidor",
            "data" : str(error),
            "status" : 500
        }