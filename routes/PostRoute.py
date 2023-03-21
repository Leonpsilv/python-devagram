import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from middlewares.JWTMiddleware import token_verify
from models.PostModel import CreatePostModel

router = APIRouter()


@router.post("/", response_description="Rota para criar um novo post.")
async def route_create_post(file: UploadFile, post: CreatePostModel = Depends(CreatePostModel)):
    try:
        photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'
        with open(photo_path, 'wb+') as archive:
            archive.write(file.file.read())

        #result = await register_user(user, photo_path)

        os.remove(photo_path)

    except Exception as error:
        raise error


@router.get(
    '/',
    response_description="Rota para listar as postagens.",
    dependencies=[Depends(token_verify)]
)
async def search_for_logged_user_infos(Authorization: str = Header(default='')):
    try:
        return {
            "test": "OK"
        }
    
    except Exception as error:
        raise error
