from api.client import ApiClient


def create_cart(token: str = None) -> dict:
    response = ApiClient(token=token).post("/carts")
    response.raise_for_status()
    return response.json()


def add_to_cart(cart_id: str, product_id: str, quantity: int, token: str = None) -> dict:
    payload = {"product_id": product_id, "quantity": quantity}
    response = ApiClient(token=token).post(f"/carts/{cart_id}", json=payload)
    response.raise_for_status()
    return response.json()


def get_cart(cart_id: str, token: str = None) -> dict:
    response = ApiClient(token=token).get(f"/carts/{cart_id}")
    response.raise_for_status()
    return response.json()


def update_quantity(cart_id: str, product_id: str, quantity: int, token: str = None) -> dict:
    payload = {"product_id": product_id, "quantity": quantity}
    response = ApiClient(token=token).put(f"/carts/{cart_id}/product/quantity", json=payload)
    response.raise_for_status()
    return response.json()


def remove_item(cart_id: str, product_id: str, token: str = None) -> None:
    ApiClient(token=token).delete(f"/carts/{cart_id}/product/{product_id}").raise_for_status()


def delete_cart(cart_id: str, token: str = None) -> None:
    ApiClient(token=token).delete(f"/carts/{cart_id}").raise_for_status()
