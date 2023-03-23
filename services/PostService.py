import os
from datetime import datetime

from bson import ObjectId

from models.PostModel import CreatePostModel
from providers.AWSProvider import AWSProvider
from repositories.PostRepository import PostRepository

awsProvider = AWSProvider()

postRepository = PostRepository()


class PostService:
    async def register_post(self, post: CreatePostModel, user_id):
        try:
            new_post = await postRepository.create_post(post, user_id)

            try:
                photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'
                with open(photo_path, 'wb+') as archive:
                    archive.write(post.photo.file.read())

                url_photo = awsProvider.upload_file_s3(f'{new_post["id"]}.png', photo_path)

                os.remove(photo_path)
                new_post = await postRepository.update_post(new_post["id"], {"photo": url_photo})
            except Exception as error:
                print(error)

            return {
                "message": "Postagem criada",
                "data": new_post,
                "status": 201
            }
        except Exception as error:
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }

    async def list_all_posts(self):
        try:
            posts = await postRepository.list_posts()
            for p in posts:
                p['total_likes'] = len(p['likes'])

            return {
                "message": "Postagens listadas com sucesso",
                "data": posts,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }

    async def like_or_unlike_post(self, post_id, user_id):
        try:
            found_post = await postRepository.search_post_by_id(post_id)
            if found_post['likes'].count(user_id) > 0:
                found_post['likes'].remove(user_id)
            else:
                found_post['likes'].append(ObjectId(user_id))

            updated_post = await postRepository.update_post(post_id, {"likes": found_post['likes']})
            return {
                "message": "Postagem curtida com sucesso",
                "data": updated_post,
                "status": 200
            }
        except Exception as error:
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }

    async def comment_post(self, post_id, user_id, comment):
        try:
            found_post = await postRepository.search_post_by_id(post_id)
            found_post['comments'].append({
                "user_id": user_id,
                "comment": comment
            })

            updated_post = await postRepository.update_post(post_id, {"comments": found_post['comments']})
            return {
                "message": "Postagem comentada com sucesso",
                "data": updated_post,
                "status": 200
            }
        except Exception as error:
            return {
                "message": "Erro interno no servidor",
                "data": str(error),
                "status": 500
            }
