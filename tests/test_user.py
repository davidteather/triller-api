import os
import TrillerAPI

user = TrillerAPI.login(
    os.environ.get("triller_username"), os.environ.get("triller_password")
)


def test_trending():
    assert len(user.get_trending(count=15)["videos"]) == 15
    assert len(user.get_trending(count=100)["videos"]) == 100


def test_trending_hashtags():
    assert len(user.get_trending_hashtags()) > 0


def test_get_user_posts_by_username():
    assert len(user.get_user_posts_by_username("chanceraps", count=6)["videos"]) == 6
    assert len(user.get_user_posts_by_username("chanceraps", count=15)["videos"]) == 15


def test_get_hashtag_object():
    assert user.get_hashtag_object("lost")["hashtag"] == "lost"


def test_get_top_posts_by_hashtag():
    assert len(user.get_top_posts_by_hashtag("lost")["videos"]) == 20
    assert len(user.get_top_posts_by_hashtag("lost", count=64)["videos"]) == 64


def test_get_new_posts_by_hashtag():
    assert len(user.get_new_posts_by_hashtag("lost")["videos"]) == 20
    assert len(user.get_new_posts_by_hashtag("lost", count=64)["videos"]) == 64


def test_user_object():
    assert user.user_object("chanceraps")["username"] == "chanceraps"


def test_like_video():
    video_id = 31333625
    assert user.like_video(video_id)


def test_follow_user():
    user_id = 14506441
    assert user.follow_user(user_id)
    assert user.unfollow_user(user_id)
