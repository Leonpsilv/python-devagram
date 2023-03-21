from decouple import config
from motor import motor_asyncio

from models.PostModel import CreatePostModel
from bson import ObjectId

from utils.AuthUtil import generate_encrypted_password

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

post_collection: object = database.get_collection('post')


def post_helper(post):
    return {
        "id": str(post["_id"]) if "_id" in post else "",
        "user": post['user'] if "user" in post else "",
        "subtitle": post['subtitle'] if "subtitle" in post else "",
        "photo": post['photo'] if "photo" in post else "",
        "date": post['date'] if "date" in post else "",
        "likes": post['likes'] if "likes" in post else "",
        "comments": post['comments'] if "comments" in post else ""
    }


async def create_post(post: CreatePostModel) -> dict:
    created_post = await post_collection.insert_one(post.__dict__)
    new_post = await post_collection.find_one({"_id": created_post.inserted_id})
    return post_helper(new_post)


async def list_posts() -> dict:
    return await post_collection.find()


async def search_post_by_id(id: str) -> dict:
    post = await post_collection.find_one({'_id': ObjectId(id)})

    if post:
        return post_helper(post)


async def delete_post (id: str):
    post = await post_collection.find_one({ "_id" : ObjectId(id) })

    if post:
        await post_collection.delete_one({ "_id" : ObjectId(id) })
    return
