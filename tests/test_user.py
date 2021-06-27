import os
import TrillerAPI
user = TrillerAPI.login(os.environ.get("triller_username"), os.environ.get("triller_password"))

def test_trending():
    assert len(user.get_trending(count=15)["videos"]) == 15
    assert len(user.get_trending(count=100)["videos"]) == 100

def test_like_video():
    video_id = 31333625
    assert user.like_video(video_id)

def test_follow_user():
    user_id = 14506441
    assert user.follow_user(user_id)
    assert user.unfollow_user(user_id)