import logging
import requests

from datetime import datetime
from .exceptions import TrillerLoginException
from .exceptions import TrillerAPIException

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login()

    def get(self, url, params={}):
        if self.token_expiration < datetime.now():
            self.login()
        params["auth_token"] = self.auth_token

        data = requests.get(url, params=params).json()

        if not data["status"]:
            raise TrillerAPIException(message=data["message"])

        return data

    def post(self, url, params={}, data={}):
        if self.token_expiration < datetime.now():
            self.login()
        params["auth_token"] = self.auth_token
        
        data = requests.post(url, params=params, data=data).json()
        
        if not data["status"]:
            raise TrillerAPIException(message=data["message"])

        return data

    def login(self):
        response = requests.post("https://social.triller.co/v1.5/user/auth", data={"username": self.username, "password": self.password}).json()
        if not response["status"]:
            raise TrillerLoginException.get("message", "Login Failed")
        self.auth_token = response["auth_token"]
        self.token_expiration = datetime.fromisoformat(response["token_expiration"])

    def get_trending(self, count=15):
        api_url = "https://social.triller.co/v1.5/api/featured"

        ads = []
        tracks = []
        users = []
        videos = []

        per_page_limit = 15
        page = 1
        while len(videos) < count:
            params = {
                "page": page,
                "limit": per_page_limit
            }
            data = self.get(api_url, params=params)
            ads.extend(data["ads"])
            tracks.extend(data["tracks"])
            users.extend(data["users"])
            videos.extend(data["videos"])

            if len(videos) == 0:
                break
            page += 1

        return {
            "ads": ads,
            "tracks": tracks,
            "users": users,
            "videos": videos[:count],
        }

    def like_video(self, video_id):
        api_url = "https://social.triller.co/v1.5/api/videos/like"
        data = self.post(api_url, {"video_id": video_id})
        return data["status"]

    def like_comment(self, comment_id):
        api_url = "https://social.triller.co/v1.5/api/comments/like"
        data = self.post(api_url, {"comment_id": comment_id})
        return data["status"]

    def comment_video(self, video_id, comment):
        api_url = f"https://social.triller.co/v1.5/api/videos/{video_id}/comments/"
        data = self.post(api_url, {"body": comment})
        return data["status"]

    def report_user(self, user_id, reason):
        api_url = "https://social.triller.co/v1.5/api/users/flag"
        data = self.post(api_url, {"flagged_user_id": user_id, "reason": reason})
        return data["status"]

    def report_video(self, video_id, reason):
        api_url = "https://social.triller.co/v1.5/api/video/flag"
        data = self.post(api_url, {"flagged_video_id": video_id, "reason": reason})
        return data["status"]

    def follow_user(self, user_id):
        api_url = "https://social.triller.co/v1.5/api/users/follow"
        data = self.post(api_url, {"followed_ids": [user_id]})
        return data["status"]

    def unfollow_user(self, user_id):
        api_url = "https://social.triller.co/v1.5/api/users/follow/delete"
        data = self.post(api_url, {"followed_ids": [user_id]})
        return data["status"]