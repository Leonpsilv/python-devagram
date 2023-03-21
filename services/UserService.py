from models.UserModel import UserCreateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import (
    create_user,
    list_users,
    search_user_by_email,
    search_user_by_id,
    edit_user,
    delete_user
)

awsProvider = AWSProvider()

async def register_user (user: UserCreateModel, photo_path):
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
            try:
                url_photo = awsProvider.upload_file_s3(f'profile-photos/{new_user["id"]}.png', photo_path)

                new_user = await edit_user(new_user["id"], {"photo" : url_photo})
            except Exception as error:
                print(error)

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