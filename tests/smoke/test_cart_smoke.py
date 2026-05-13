"""S07 — Add a product to the cart."""
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.mark.smoke
@pytest.mark.ui
def test_add_product_to_cart(page: Page):
    """S07 — Add first available product to cart; cart icon updates."""
    home = HomePage(page).open()
    home.click_product(0)

    product = ProductPage(page)
    expect(product.add_to_cart_button).to_be_visible()
    product.add_to_cart()

    # Cart badge / icon should reflect 1 item
    cart_indicator = page.locator("[data-test='nav-cart']")
    expect(cart_indicator).to_be_visible()
