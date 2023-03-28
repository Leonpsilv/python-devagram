from typing import List

from decouple import config
from motor import motor_asyncio
from models.UserModel import UserCreateModel, UserModel
from bson import ObjectId

from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

user_collection: object = database.get_collection('user')
converterUtil = ConverterUtil()
authUtil = AuthUtil()


class UserRepository:
    async def create_user(self, user: UserCreateModel) -> UserModel:
        user.password = authUtil.generate_encrypted_password(user.password)

        user_dict = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "followers": [],
            "following": []
        }

        created_user = await user_collection.insert_one(user_dict)

        new_user = await user_collection.find_one({"_id": created_user.inserted_id})

        return converterUtil.user_converter(new_user)

    async def list_users(self, name) -> List[UserModel]:
        founded_users = user_collection.find({
            "name": {
                "$regex": name,
                '$options': 'i' # case insensitive
            }
        })
        users = []

        async for user in founded_users:
            user_data = converterUtil.user_converter(user)
            del user_data['password']

            users.append(user_data)

        return users

    async def search_user_by_email(self, email: str) -> UserModel:
        user = await user_collection.find_one({"email": email})
        if user:
            return converterUtil.user_converter(user)
        else:
            return

    async def edit_user(self, id: str, user_data: dict) -> UserModel:
        user = await user_collection.find_one({"_id": ObjectId(id)})
        if "password" in user_data:
            user_data['password'] = authUtil.generate_encrypted_password(user_data['password'])
        if user:
            await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": user_data}
            )
            edited_user = await user_collection.find_one({"_id": ObjectId(id)})
            return converterUtil.user_converter(edited_user)

    async def delete_user(self, id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            await user_collection.delete_one({"_id": ObjectId(id)})
            return {"message": "usuario deletado!"}
        else:
            return

    async def search_user_by_id(self, id: str) -> UserModel:
        user = await user_collection.find_one({'_id': ObjectId(id)})

        if user:
            return converterUtil.user_converter(user)
