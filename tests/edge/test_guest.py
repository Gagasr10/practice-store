"""E01 — Guest checkout via API."""
import pytest

import api.cart as cart_api
import api.products as products_api
from api.invoices import create_guest_invoice
from data.test_data import DEFAULT_ADDRESS, PAYMENT_COD


@pytest.mark.edge
@pytest.mark.api
@pytest.mark.xfail(
    reason="POST /invoices/guest returns 404 — endpoint not available in current API version",
    strict=False,
)
def test_guest_checkout_via_api():
    # 1. Get a valid product
    data = products_api.get_products()
    product_id = (data["data"] if "data" in data else data)[0]["id"]

    # 2. Create a cart and add the product
    cart = cart_api.create_cart()
    cart_id = cart["id"]
    cart_api.add_to_cart(cart_id, product_id, quantity=1)

    # 3. Submit a guest invoice
    payload = {
        "cart_id": cart_id,
        "billing_address": DEFAULT_ADDRESS,
        "payment": PAYMENT_COD,
    }
    resp = create_guest_invoice(payload)
    assert resp.get("id") or resp.get("invoice_number"), (
        f"Guest checkout did not return an invoice: {resp}"
    )
