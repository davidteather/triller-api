import logging
import requests

from datetime import datetime
from .exceptions import TrillerLoginException
from .exceptions import TrillerAPIException


class User:
    """This represents a Triller account"""

    username: str
    password: str
    auth_token: str
    token_expiration: str
    triller_id: str

    def __init__(self, username: str, password: str):
        """Create and log into a Triller user's account."""
        self.username = username
        self.password = password
        self.login()

    def login(self):
        """Performs the log in action for a Triller user."""
        response = requests.post(
            "https://social.triller.co/v1.5/user/auth",
            data={"username": self.username, "password": self.password},
        ).json()
        if not response["status"]:
            raise TrillerLoginException(message=response.get("message", "Login Failed"))
        self.auth_token = response["auth_token"]
        self.token_expiration = datetime.fromisoformat(response["token_expiration"])
        self.triller_id = response["user"]["user_id"]

    def get_trending_hashtags(self):
        """Retrieves trending hashtags"""
        api_url = "https://social.triller.co/v1.5/api/hash_tags/trending"
        return self.__get(api_url)["hash_tags"]

    def get_trending(self, count=15):
        """Retrieves trending ads, tracks, users, and videos."""
        api_url = "https://social.triller.co/v1.5/api/featured"
        ads = []
        tracks = []
        users = []
        videos = []
        per_page_limit = 15
        page = 1
        while len(videos) < count:
            params = {"page": page, "limit": per_page_limit}
            data = self.__get(api_url, params=params)
            ads.extend(data["ads"])
            tracks.extend(data["tracks"])
            users.extend(data["users"])
            pre_extension_length = len(videos)
            videos.extend(data["videos"])
            if pre_extension_length == len(videos):
                break

            if len(videos) == 0:
                break
            page += 1

        return {
            "ads": ads,
            "tracks": tracks,
            "users": users,
            "videos": videos[:count],
        }

    def get_user_posts(self, user_id, count=6):
        """Retrieves a user's posts given a user's id"""
        api_url = f"https://social.triller.co/v1.5/api/users/{user_id}/videos"
        users = []
        videos = []
        per_page_limit = 6
        before_time = datetime.now().isoformat()
        while len(videos) < count:
            params = {"before_time": before_time, "limit": per_page_limit}
            data = self.__get(api_url, params=params)
            users.extend(data["users"])
            pre_extension_length = len(videos)
            videos.extend(data["videos"])
            if pre_extension_length == len(videos):
                break

            if len(videos) == 0:
                break
            before_time = data["videos"][-1]["timestamp"]

        return {
            "users": users,
            "videos": videos[:count],
        }

    def get_user_posts_by_username(self, username, count=6):
        """Retrieves a user's posts given a username"""
        user_id = self.user_object(username)["user_id"]
        return self.get_user_posts(user_id, count=count)

    def get_hashtag_object(self, hashtag: str):
        """Retrieves a hashtag object for a hashtag's plaintext name."""
        api_url = f"https://social.triller.co/v1.5/api/hash_tags/challenge?hash_tag_name={hashtag}"
        return self.__get(api_url)

    def get_top_posts_by_hashtag(self, hashtag: str, count=20):
        """Retrieves top posts under a hashtag"""
        api_url = f"https://social.triller.co/v1.5/api/hash_tags/top"

        users = []
        videos = []
        page = 1
        while len(videos) < count:
            params = {"page": page, "hash_tag": hashtag}
            data = self.__get(api_url, params=params)
            users.extend(data["users"])
            pre_extension_length = len(videos)
            videos.extend(data["videos"])
            if pre_extension_length == len(videos):
                break

            if len(videos) == 0:
                break
            page += 1

        return {
            "users": users,
            "videos": videos[:count],
        }

    def get_new_posts_by_hashtag(self, hashtag: str, count=20):
        """Retrieves new posts under a hashtag"""
        api_url = f"https://social.triller.co/v1.5/api/hash_tags/fresh"

        users = []
        videos = []
        page = 1
        while len(videos) < count:
            params = {"page": page, "hash_tag": hashtag}
            data = self.__get(api_url, params=params)
            users.extend(data["users"])

            pre_extension_length = len(videos)
            videos.extend(data["videos"])
            if pre_extension_length == len(videos):
                break

            if len(videos) == 0:
                break
            page += 1

        return {
            "users": users,
            "videos": videos[:count],
        }

    def user_object(self, username: str):
        """Retrieves a user object given a username"""
        api_url = f"https://social.triller.co/v1.5/api/users/by_username/{username}"
        return self.__get(api_url)["user"]

    def like_video(self, video_id):
        """Likes a video given a video's id"""
        api_url = "https://social.triller.co/v1.5/api/videos/like"
        data = self.__post(api_url, {"video_id": video_id})
        return data["status"]

    def like_comment(self, comment_id):
        """Likes a comment given a comment's id"""
        api_url = "https://social.triller.co/v1.5/api/comments/like"
        data = self.__post(api_url, {"comment_id": comment_id})
        return data["status"]

    def comment_video(self, video_id, comment):
        """Comments on a video given the video's ID and the comment's body"""
        api_url = f"https://social.triller.co/v1.5/api/videos/{video_id}/comments/"
        data = self.__post(api_url, {"body": comment})
        return data["status"]

    def report_user(self, user_id, reason):
        """Reports a user given a user's id and a reason"""
        api_url = "https://social.triller.co/v1.5/api/users/flag"
        data = self.__post(api_url, {"flagged_user_id": user_id, "reason": reason})
        return data["status"]

    def report_video(self, video_id, reason):
        """Reports a video given a video's id and a reason"""
        api_url = "https://social.triller.co/v1.5/api/video/flag"
        data = self.__post(api_url, {"flagged_video_id": video_id, "reason": reason})
        return data["status"]

    def follow_user(self, user_id):
        """Follows a user given a user's id (Triller account logged into must have email verified)"""
        api_url = "https://social.triller.co/v1.5/api/users/follow"
        data = self.__post(
            api_url, {"followed_ids": [user_id], "follower_id": self.triller_id}
        )
        return data["status"]

    def unfollow_user(self, user_id):
        """Unfollows a user given a user's id"""
        api_url = "https://social.triller.co/v1.5/api/users/follow/delete"
        data = self.__post(
            api_url, {"followed_ids": [user_id], "follower_id": self.triller_id}
        )
        return data["status"]

    #
    # Private Methods
    #
    def __get(self, url, params={}):
        if self.token_expiration < datetime.now():
            self.login()
        params["auth_token"] = self.auth_token

        data = requests.get(url, params=params).json()

        if not data.get("status", True):
            raise TrillerAPIException(message=data["message"])

        return data

    def __post(self, url, params={}, data={}):
        if self.token_expiration < datetime.now():
            self.login()
        params["auth_token"] = self.auth_token

        data = requests.post(url, params=params, data=data).json()

        if not data["status"]:
            raise TrillerAPIException(message=data["message"])

        return data
