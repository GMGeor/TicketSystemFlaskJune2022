from managers.auth import AuthManager


def generate_token(user):
    token = AuthManager.encode_token(user)
    return token


def generate_headers(user):
    token = generate_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    return headers
