import os
from datetime import datetime

from bson import ObjectId

from dtos.ResponseDTO import ResponseDTO
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

                url_photo = awsProvider.upload_file_s3(f'{new_post.id}.png', photo_path)
                new_post = await postRepository.update_post(new_post.id, {"photo": url_photo})
                os.remove(photo_path)
            except Exception as error:
                print(error)

            return ResponseDTO("Postagem criada", new_post, 201)

        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def list_all_posts(self):
        try:
            posts = await postRepository.list_posts()
            for p in posts:
                p.total_likes = len(p.likes)
                p.total_comments = len(p.comments)

            return ResponseDTO("Postagens listadas com sucesso", posts, 200)
        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def list_all_user_posts(self, user_id):
        try:
            posts = await postRepository.list_user_posts(user_id)
            for p in posts:
                p['total_likes'] = len(p['likes'])
                p['total_comments'] = len(p['comments'])

            return ResponseDTO("Postagens do usuário listadas com sucesso", posts, 200)
        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def like_or_unlike_post(self, post_id, user_id):
        try:
            found_post = await postRepository.search_post_by_id(post_id)
            if found_post.likes.count(user_id) > 0:
                found_post.likes.remove(user_id)
            else:
                found_post.likes.append(ObjectId(user_id))

            updated_post = await postRepository.update_post(post_id, {"likes": found_post.likes})

            return ResponseDTO("Postagem curtida/descurtida com sucesso", updated_post, 200)
        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def comment_post(self, post_id, user_id, comment):
        try:
            found_post = await postRepository.search_post_by_id(post_id)
            found_post.comments.append({
                "comment_id": ObjectId(),
                "user_id": user_id,
                "comment": comment
            })

            updated_post = await postRepository.update_post(post_id, {"comments": found_post.comments})

            return ResponseDTO("Postagem comentada com sucesso", updated_post, 200)

        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def delete_comment_post(self, post_id, user_id, comment_id):
        try:
            found_post = await postRepository.search_post_by_id(post_id)

            for comment in found_post.comments:
                if comment['comment_id'] == comment_id:
                    if not (comment['user_id'] == user_id or found_post.user_id == user_id):
                        return ResponseDTO("Requisição inválida.", "", 401)

                    found_post.comments.remove(comment)

            updated_post = await postRepository.update_post(post_id, {"comments": found_post.comments})

            return ResponseDTO("Comentário removido com sucesso", updated_post, 200)
        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def edit_comment_post(self, post_id, user_id, comment_id, updated_comment):
        try:
            found_post = await postRepository.search_post_by_id(post_id)

            for comment in found_post.comments:
                if comment['comment_id'] == comment_id:
                    if not comment['user_id'] == user_id:
                        return ResponseDTO("Requisição inválida.", "", 401)

                    comment['comment'] = updated_comment

            updated_post = await postRepository.update_post(post_id, {"comments": found_post.comments})

            return ResponseDTO("Comentário atualizado com sucesso.", updated_post, 200)

        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)

    async def delete_post(self, post_id, user_id):
        try:
            found_post = await postRepository.search_post_by_id(post_id)

            if not found_post:
                return ResponseDTO("Postagem não encontrada.", "", 404)

            if not found_post.user_id == user_id:
                return ResponseDTO("Não é possível realizar essa requisição.", "", 401)

            await postRepository.delete_post(post_id)
            return ResponseDTO("Postagem deletada com sucesso!", "", 200)

        except Exception as error:
            return ResponseDTO("Erro interno no servidor", str(error), 500)
