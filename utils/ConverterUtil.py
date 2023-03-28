from models.PostModel import PostModel
from models.UserModel import UserModel


class ConverterUtil:
    def user_converter(self, user):
        return UserModel(
            id = str(user["_id"]),
            name = user['name'],
            email = user['email'],
            password = user['password'],
            photo = user['photo'] if "photo" in user else "",  # if ternário
            followers = [str(p) for p in user['followers']] if "followers" in user else [],
            following = [str(p) for p in user['following']] if "following" in user else [],
            total_followers = user("total_followers") if "total_followers" in user else 0,
            total_following = user("total_following") if "total_following" in user else 0,
            all_posts = user("all_posts") if "all_posts" in user else [],
            total_posts = user("total_posts") if "total_posts" in user else 0,
            token=user['token'] if "token" in user else "",
        )

    def post_converter(self, post):
        return PostModel(
            id = str(post["_id"]) if "_id" in post else "",
            user_id = str(post['user_id']) if "user_id" in post else "",
            subtitle = post['subtitle'] if "subtitle" in post else "",
            photo = post['photo'] if "photo" in post else "",
            date = str(post['date']) if "date" in post else "",
            likes = [str(p) for p in post['likes']] if "likes" in post else [],
            comments = [
                {
                    "comment_id": str(p['comment_id']),
                    "user_id": str(p['user_id']),
                    "comment": str(p['comment']),

                } for p in post['comments']] if "comments" in post else [],
            user = self.user_converter(post['user'][0]) if 'user' in post and len(post['user']) > 0 else None,
            total_likes = post["total_likes"] if "total_likes" in post else 0,
            total_comments = post["total_comments"] if "total_comments" in post else 0,
        )

