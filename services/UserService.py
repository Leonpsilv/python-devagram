import os
from datetime import datetime

from bson import ObjectId

from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository
from repositories.PostRepository import PostRepository

awsProvider = AWSProvider()

userRepository = UserRepository()
postRepository = PostRepository()


class UserService:
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
                    os.remove(photo_path)
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
            found_posts = await postRepository.list_user_posts(id)

            found_user["total_following"] = len(found_user["following"])
            found_user["total_followers"] = len(found_user["followers"])
            found_user["all_posts"] = found_posts
            found_user["total_posts"] = len(found_posts)

            if found_user:
                return {
                    "message" : "Usuário encontrado com sucesso",
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

    async def search_all_users(self, name):
        try:
            found_users = await userRepository.list_users(name)

            for user in found_users:
                user["total_following"] = len(user["following"])
                user["total_followers"] = len(user["followers"])

            return {
                "message" : "Usuários listados com sucesso.",
                "data" : found_users,
                "status": 200
            }

        except Exception as error:
            print(error)
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

    async def follow_or_unfollow_user(self, user_id, followed_user_id):
        try:
            found_followed_user = await userRepository.search_user_by_id(followed_user_id)
            found_following_user = await userRepository.search_user_by_id(user_id)

            if not found_followed_user or not found_following_user:
                return {
                "message": "Usuário não encontrado",
                "data": "",
                "status": 404
            }

            if found_followed_user['followers'].count(user_id) > 0:
                found_followed_user['followers'].remove(user_id)
                found_following_user['following'].remove(followed_user_id)
            else:
                found_followed_user['followers'].append(ObjectId(user_id))
                found_following_user['following'].append(ObjectId(followed_user_id))

            await userRepository.edit_user(followed_user_id, {"followers": found_followed_user['followers']})
            await userRepository.edit_user(user_id, {"following": found_following_user['following']})

            return {
                "message": "Requisição realizada com sucesso",
                "data": "",
                "status": 200
            }
        except Exception as error:
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }