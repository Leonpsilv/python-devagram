from fastapi import APIRouter, HTTPException, Depends, Header, Body

from middlewares.JWTMiddleware import token_verify
from models.CommentModel import CreateCommentModel, EditCommentModel
from models.PostModel import CreatePostModel
from services.AuthService import AuthService
from services.UserService import UserService
from services.PostService import PostService

router = APIRouter()
userService = UserService()
postService = PostService()
authService = AuthService()


@router.post(
    "/",
    response_description="Rota para criar um novo post.",
    dependencies=[Depends(token_verify)]
)
async def route_create_post(
        Authorization: str = Header(default=''),
        post: CreatePostModel = Depends(CreatePostModel)
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.register_post(post, logged_user['id'])

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.get(
    "/",
    response_description="Rota para listar postagens.",
    dependencies=[Depends(token_verify)]
)
async def list_all_posts():
    try:
        result = await postService.list_all_posts()

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.get(
    "/{user_id}",
    response_description="Rota para listar as postagens de um usuário específico.",
    dependencies=[Depends(token_verify)]
)
async def list_all_user_posts(user_id: str):
    try:
        result = await postService.list_all_user_posts(user_id)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.put(
    "/like/{post_id}",
    response_description="Rota para curtir/descurtir uma postagem.",
    dependencies=[Depends(token_verify)]
)
async def like_unlike_post(
        post_id: str,
        Authorization: str = Header(default='')
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.like_or_unlike_post(post_id, logged_user['id'])

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.put(
    "/comentar/{post_id}",
    response_description="Rota para comentar em uma postagem.",
    dependencies=[Depends(token_verify)]
)
async def comment_a_post(
        post_id: str,
        Authorization: str = Header(default=''),
        comment_model: CreateCommentModel = Body(...)
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.comment_post(post_id, logged_user['id'], comment_model.comment)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.delete(
    "/{post_id}/comentar/{comment_id}",
    response_description="Rota para deletar um comentário em uma postagem.",
    dependencies=[Depends(token_verify)]
)
async def delete_post_comment(
        post_id: str,
        comment_id: str,
        Authorization: str = Header(default=''),
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.delete_comment_post(post_id, logged_user['id'], comment_id)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.put(
    "/{post_id}/comentar/{comment_id}",
    response_description="Rota para editar um comentário em uma postagem.",
    dependencies=[Depends(token_verify)]
)
async def edit_post_comment(
        post_id: str,
        comment_id: str,
        Authorization: str = Header(default=''),
        edited_comment: EditCommentModel = Body(...)
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.edit_comment_post(post_id, logged_user['id'], comment_id, edited_comment.comment)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error


@router.delete(
    "/{post_id}",
    response_description="Rota para deletar uma postagem.",
    dependencies=[Depends(token_verify)]
)
async def delete_a_post(
        post_id: str,
        Authorization: str = Header(default='')
):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decode_token_jwt(token)
        result_user = await (userService.search_user(payload["user_id"]))
        logged_user = result_user['data']

        result = await postService.delete_post(post_id, logged_user['id'])

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        return result
    except Exception as error:
        raise error
