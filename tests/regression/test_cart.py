"""R21-R26 — Cart regression tests."""
import pytest
from playwright.sync_api import Page, expect

import api.cart as cart_api
import api.products as products_api
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from data.test_data import BASE_URL


@pytest.mark.regression
@pytest.mark.ui
def test_add_multiple_products_to_cart(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")

    user_page.goto(BASE_URL)
    user_page.wait_for_selector("a[data-test^='product-']", state="visible", timeout=30_000)
    home.click_product(1)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")

    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    user_page.wait_for_load_state("networkidle")
    cart = CartPage(user_page)
    expect(cart.items.first).to_be_visible(timeout=15_000)
    assert cart.get_item_count() >= 2


@pytest.mark.regression
@pytest.mark.ui
def test_update_item_quantity_in_cart(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")

    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    user_page.wait_for_load_state("networkidle")
    qty_input = user_page.locator("[data-test='product-quantity']").first
    qty_input.fill("3")
    qty_input.press("Tab")
    expect(qty_input).to_have_value("3", timeout=4_000)


@pytest.mark.regression
@pytest.mark.ui
def test_remove_single_item_from_cart(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")

    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    user_page.wait_for_load_state("networkidle")
    cart = CartPage(user_page)
    expect(cart.items.first).to_be_visible(timeout=15_000)
    initial_count = cart.get_item_count()
    cart.remove_item(0)
    expect(user_page.locator("[data-test='product-title']")).to_have_count(
        initial_count - 1, timeout=8_000
    )


@pytest.mark.regression
@pytest.mark.ui
def test_cart_persists_across_navigation(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")

    # Navigate away via SPA links, then back via nav-cart to avoid auth-guard race
    user_page.locator("[data-test='nav-contact']").click()
    user_page.wait_for_url("**/contact**", timeout=8_000)
    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    user_page.wait_for_load_state("networkidle")
    cart = CartPage(user_page)
    expect(cart.items.first).to_be_visible(timeout=15_000)
    assert cart.get_item_count() > 0


@pytest.mark.regression
@pytest.mark.api
def test_api_create_cart_and_add_item():
    data = products_api.get_products()
    product_id = (data["data"] if "data" in data else data)[0]["id"]

    cart = cart_api.create_cart()
    cart_id = cart["id"]
    try:
        cart_api.add_to_cart(cart_id, product_id, quantity=2)
        cart_data = cart_api.get_cart(cart_id)
        items = cart_data.get("cart_items", cart_data.get("items", []))
        assert any(item.get("product_id") == product_id for item in items), (
            f"Product {product_id} not found in cart after adding"
        )
    finally:
        cart_api.delete_cart(cart_id)


@pytest.mark.regression
@pytest.mark.api
def test_api_remove_item_from_cart():
    data = products_api.get_products()
    product_id = (data["data"] if "data" in data else data)[0]["id"]

    cart = cart_api.create_cart()
    cart_id = cart["id"]
    try:
        cart_api.add_to_cart(cart_id, product_id, quantity=1)
        cart_api.remove_item(cart_id, product_id)
        cart_data = cart_api.get_cart(cart_id)
        items = cart_data.get("cart_items", cart_data.get("items", []))
        assert not any(item.get("product_id") == product_id for item in items), (
            f"Product {product_id} still in cart after removal"
        )
    finally:
        cart_api.delete_cart(cart_id)
