from api.client import ApiClient


def login(email: str, password: str) -> dict:
    client = ApiClient()
    response = client.post("/users/login", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()


def logout(token: str) -> None:
    ApiClient(token=token).get("/users/logout")


def refresh_token(token: str) -> dict:
    response = ApiClient(token=token).get("/users/refresh")
    response.raise_for_status()
    return response.json()


def get_me(token: str) -> dict:
    response = ApiClient(token=token).get("/users/me")
    response.raise_for_status()
    return response.json()
