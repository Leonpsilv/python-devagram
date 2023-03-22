from decouple import config
from motor import motor_asyncio

from models.PostModel import CreatePostModel
from bson import ObjectId

from utils.ConverterUtil import ConverterUtil

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

post_collection: object = database.get_collection('post')

converterUtil = ConverterUtil()


class PostRepository:
    async def create_post(self, post: CreatePostModel) -> dict:
        created_post = await post_collection.insert_one(post.__dict__)
        new_post = await post_collection.find_one({"_id": created_post.inserted_id})
        return converterUtil.post_converter(new_post)

    async def list_posts(self) -> dict:
        return await post_collection.find()

    async def search_post_by_id(self, id: str) -> dict:
        post = await post_collection.find_one({'_id': ObjectId(id)})

        if post:
            return converterUtil.post_converter(post)

    async def delete_post(self, id: str):
        post = await post_collection.find_one({"_id": ObjectId(id)})

        if post:
            await post_collection.delete_one({"_id": ObjectId(id)})
        return
