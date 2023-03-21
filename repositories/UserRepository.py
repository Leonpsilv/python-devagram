from decouple import config
from motor import motor_asyncio
from models.UserModel import UserCreateModel
from bson import ObjectId

from utils.AuthUtil import generate_encrypted_password

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

user_collection: object = database.get_collection('user')


def user_helper(user):
    return {
        "id": str(user["_id"]),
        "name": user['name'],
        "email": user['email'],
        "password": user['password'],
        "photo": user['photo'] if "photo" in user else "" #if ternário
    }


async def create_user(user: UserCreateModel) -> dict:
    user.password = generate_encrypted_password(user.password)

    created_user = await user_collection.insert_one(user.__dict__)
    new_user = await user_collection.find_one({"_id": created_user.inserted_id})
    return user_helper(new_user)


async def list_users() -> dict:
    return await user_collection.find()


async def search_user_by_email(email: str) -> dict:
    user = await user_collection.find_one({"email" : email})
    if user:
        return user_helper(user)
    else:
        return


async def edit_user(id: str, user_data: dict):
    user = await user_collection.find_one({ "_id" : ObjectId(id) })

    if user:
        edited_user = await user_collection.update_one(
            {"_id" : ObjectId(id)}, {"$set" : user_data}
        )
        return user_helper(edited_user)
    else:
        return


async def delete_user (id: str):
    user = await user_collection.find_one({ "_id" : ObjectId(id) })

    if user:
        await user_collection.delete_one({ "_id" : ObjectId(id) })
        return {"message" : "usuario deletado!"}
    else:
        return


async def search_user_by_id(id: str) -> dict:
    user = await user_collection.find_one({'_id': ObjectId(id)})

    if user:
        return user_helper(user)
