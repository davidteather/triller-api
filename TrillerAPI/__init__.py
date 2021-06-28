from .user import User


def login(username, password):
    return User(username, password)
