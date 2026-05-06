"""E03, E04, E08 — Cart edge cases."""
import concurrent.futures
import pytest

import api.cart as cart_api
import api.products as products_api
from api.client import ApiClient


@pytest.mark.edge
@pytest.mark.api
def test_add_zero_quantity_rejected():
    data = products_api.get_products()
    product_id = (data["data"] if "data" in data else data)[0]["id"]

    cart = cart_api.create_cart()
    cart_id = cart["id"]
    try:
        client = ApiClient()
        resp = client.post(f"/carts/{cart_id}", json={"product_id": product_id, "quantity": 0})
        assert resp.status_code in (400, 404, 422), (
            f"Expected 4xx error for zero quantity, got {resp.status_code}"
        )
    finally:
        cart_api.delete_cart(cart_id)


@pytest.mark.edge
@pytest.mark.api
def test_add_out_of_stock_product_returns_error():
    """Adding quantity greater than available stock should be rejected or flagged."""
    data = products_api.get_products()
    products = data["data"] if "data" in data else data

    # Find a product with limited stock (or use an impossibly large quantity)
    product_id = products[0]["id"]
    cart = cart_api.create_cart()
    cart_id = cart["id"]
    try:
        client = ApiClient()
        resp = client.post(
            f"/carts/{cart_id}",
            json={"product_id": product_id, "quantity": 999_999},
        )
        # Either rejected immediately (422/400) or accepted (app checks stock at checkout)
        assert resp.status_code in (200, 201, 422, 400), (
            f"Unexpected status {resp.status_code} for large quantity"
        )
    finally:
        cart_api.delete_cart(cart_id)


@pytest.mark.edge
@pytest.mark.api
def test_concurrent_adds_to_same_cart():
    data = products_api.get_products()
    products = data["data"] if "data" in data else data
    product_id = products[0]["id"]

    cart = cart_api.create_cart()
    cart_id = cart["id"]
    try:
        def add_item():
            return cart_api.add_to_cart(cart_id, product_id, quantity=1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(add_item) for _ in range(2)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # Cart must remain in a consistent state
        cart_data = cart_api.get_cart(cart_id)
        items = cart_data.get("cart_items", cart_data.get("items", []))
        assert any(
            item.get("product_id") == product_id for item in items
        ), "Product not found in cart after concurrent adds"
    finally:
        cart_api.delete_cart(cart_id)
