class ConverterUtil:
    def user_converter(self, user):
        return {
            "id": str(user["_id"]),
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],
            "photo": user['photo'] if "photo" in user else ""  # if ternário
        }

    def post_converter(self, post):
        return {
            "id": str(post["_id"]) if "_id" in post else "",
            "user_id": str(post['user_id']) if "user_id" in post else "",
            "subtitle": post['subtitle'] if "subtitle" in post else "",
            "photo": post['photo'] if "photo" in post else "",
            "date": post['date'] if "date" in post else "",
            "likes": post['likes'] if "likes" in post else "",
            "comments": post['comments'] if "comments" in post else "",
            "user": self.user_converter(post['user'][0]) if len (post['user']) > 0 else ""
        }

