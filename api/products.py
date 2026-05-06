from api.client import ApiClient


def get_products(token: str = None, params: dict = None) -> dict:
    response = ApiClient(token=token).get("/products", params=params)
    response.raise_for_status()
    return response.json()


def get_product(product_id: str, token: str = None) -> dict:
    response = ApiClient(token=token).get(f"/products/{product_id}")
    response.raise_for_status()
    return response.json()


def search_products(query: str, token: str = None) -> dict:
    response = ApiClient(token=token).get("/products/search", params={"q": query})
    response.raise_for_status()
    return response.json()


def get_categories(token: str = None) -> list:
    response = ApiClient(token=token).get("/categories")
    response.raise_for_status()
    return response.json()


def get_categories_tree(token: str = None) -> list:
    response = ApiClient(token=token).get("/categories/tree")
    response.raise_for_status()
    return response.json()


def create_product(payload: dict, token: str) -> dict:
    response = ApiClient(token=token).post("/products", json=payload)
    response.raise_for_status()
    return response.json()


def delete_product(product_id: str, token: str) -> None:
    ApiClient(token=token).delete(f"/products/{product_id}").raise_for_status()
