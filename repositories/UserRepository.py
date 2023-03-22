from decouple import config
from motor import motor_asyncio
from models.UserModel import UserCreateModel
from bson import ObjectId

from utils.AuthUtil import generate_encrypted_password
from utils.ConverterUtil import ConverterUtil

MONGO_URL = config("MONGO_URL")
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.devagram

user_collection: object = database.get_collection('user')
converterUtil = ConverterUtil()


class UserRepository:
    async def create_user(self, user: UserCreateModel) -> dict:
        user.password = generate_encrypted_password(user.password)
        created_user = await user_collection.insert_one(user.__dict__)
        new_user = await user_collection.find_one({"_id": created_user.inserted_id})
        return converterUtil.user_converter(new_user)

    async def list_users(self) -> dict:
        return await user_collection.find()

    async def search_user_by_email(self, email: str) -> dict:
        user = await user_collection.find_one({"email": email})
        if user:
            return converterUtil.user_converter(user)
        else:
            return

    async def edit_user(self, id: str, user_data: dict):
        user = await user_collection.find_one({"_id": ObjectId(id)})
        if "password" in user_data:
            user_data['password'] = generate_encrypted_password(user_data['password'])
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

    async def search_user_by_id(self, id: str) -> dict:
        user = await user_collection.find_one({'_id': ObjectId(id)})

        if user:
            return converterUtil.user_converter(user)
