class ConverterUtil:
    def user_converter(self, user):
        return {
            "id": str(user["_id"]),
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],
            "photo": user['photo'] if "photo" in user else "",  # if ternário
            "followers": [str(p) for p in user['followers']] if "followers" in user else "",
            "following": [str(p) for p in user['following']] if "following" in user else "",
        }

    def post_converter(self, post):
        return {
            "id": str(post["_id"]) if "_id" in post else "",
            "user_id": str(post['user_id']) if "user_id" in post else "",
            "subtitle": post['subtitle'] if "subtitle" in post else "",
            "photo": post['photo'] if "photo" in post else "",
            "date": post['date'] if "date" in post else "",
            "likes": [str(p) for p in post['likes']] if "likes" in post else "",
            "comments": [
                {
                    "comment_id": str(p['comment_id']),
                    "user_id": str(p['user_id']),
                    "comment": str(p['comment']),

                } for p in post['comments']] if "comments" in post else "uau",
            "user": self.user_converter(post['user'][0]) if 'user' in post and len (post['user']) > 0 else ""
        }

