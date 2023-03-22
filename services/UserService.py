from datetime import datetime

from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository

awsProvider = AWSProvider()

userRepository = UserRepository()
class UserService():
    async def register_user(self, user: UserCreateModel, photo_path):
        try:
            found_user = await userRepository.search_user_by_email(user.email)
            if found_user:
                return {
                    "message": "Este email já está cadastrado!",
                    "data": "",
                    "status": 400
                }
            else:
                new_user = await userRepository.create_user(user)
                try:
                    url_photo = awsProvider.upload_file_s3(f'profile-photos/{new_user["id"]}.png', photo_path)

                    new_updated_user = await userRepository.edit_user(new_user["id"], {"photo": url_photo})
                except Exception as error:
                    print(error)

                return {
                    "message": "Usuário cadastrado com sucesso!",
                    "data": new_updated_user,
                    "status": 201
                }
        except Exception as error:
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }

    async def search_user(self, id: str):
        try:
            found_user = await userRepository.search_user_by_id(id)
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

    async def update_logged_user(self, id, update_user: UserUpdateModel):
        try:
            found_user = await userRepository.search_user_by_id(id)
            if found_user:
                photo_upload = update_user.photo
                user_dict = update_user.__dict__

                try:
                    photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'
                    with open(photo_path, 'wb+') as archive:
                        archive.write(photo_upload.file.read())

                    url_photo = awsProvider.upload_file_s3(
                        f'profile-photos/{id}.png',
                        photo_path
                    )
                except Exception as error:
                    print(error)

                user_dict['photo'] = url_photo if url_photo is not None else user_dict['photo']
                updated_user = await userRepository.edit_user(id, user_dict)
                return {
                    "message": "Usuário atualizado com sucesso!",
                    "data": updated_user,
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