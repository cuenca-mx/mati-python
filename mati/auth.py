from base64 import b64encode


def basic_auth_str(username: str, password: str) -> str:
    auth = b64encode(f'{username}:{password}'.encode('utf-8'))
    return 'Basic ' + auth.decode('ascii')


def bearer_auth_str(access_token: str) -> str:
    return f'Bearer {access_token}'
