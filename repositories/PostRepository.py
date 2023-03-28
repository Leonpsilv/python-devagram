from datetime import datetime
from typing import List

from decouple import config
from motor import motor_asyncio

from models.PostModel import CreatePostModel, PostModel
from bson import ObjectId

from utils.ConverterUtil import ConverterUtil

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

post_collection: object = database.get_collection('post')

converterUtil = ConverterUtil()


class PostRepository:
    async def update_post(self, id: str, post_data: dict) -> PostModel:
        post = await post_collection.find_one({"_id": ObjectId(id)})

        if post:
            await post_collection.update_one({"_id" : ObjectId(id)}, {"$set": post_data})
            updated_post = await post_collection.find_one({"_id": ObjectId(id)})

            return converterUtil.post_converter(updated_post)

    async def create_post(self, post: CreatePostModel, user_id) -> PostModel:
        post_dict = {
            'user_id': ObjectId(user_id),
            'subtitle': post.subtitle,
            'likes': [],
            'comments': [],
            'date': datetime.now()
        }
        created_post = await post_collection.insert_one(post_dict)
        new_post = await post_collection.find_one({"_id": created_post.inserted_id})
        return converterUtil.post_converter(new_post)

    async def list_posts(self) -> List[PostModel]:
        founded_posts = post_collection.aggregate([
            {
                "$lookup": {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            }
        ])
        posts = []
        async for post in founded_posts:
            posts.append(converterUtil.post_converter(post))

        return posts

    async def list_user_posts(self, user_id) -> List[PostModel]:
        founded_posts = post_collection.aggregate([
            {
              "$match": {
                  "user_id": ObjectId(user_id)
              }
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            }
        ])
        posts = []
        async for post in founded_posts:
            posts.append(converterUtil.post_converter(post))

        return posts

    async def search_post_by_id(self, id: str) -> PostModel:
        post = await post_collection.find_one({"_id": ObjectId(id)})
        if post:
            return converterUtil.post_converter(post)

    async def delete_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})

        if post:
            await post_collection.delete_one({"_id": ObjectId(id)})
        return
