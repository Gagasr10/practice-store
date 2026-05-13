"""S04, S05, S06 — Product listing, detail page, and search."""
import pytest
from playwright.sync_api import Page, expect

import api.products as products_api
from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.mark.smoke
@pytest.mark.api
def test_product_listing_api_returns_results():
    """S04 — GET /products returns a non-empty list."""
    data = products_api.get_products()
    assert "data" in data or isinstance(data, list)
    items = data["data"] if "data" in data else data
    assert len(items) > 0, "Product listing API returned empty list"


@pytest.mark.smoke
@pytest.mark.ui
def test_product_detail_page_loads(page: Page):
    """S05 — Clicking a product opens its detail page."""
    home = HomePage(page).open()
    home.click_product(0)
    product = ProductPage(page)
    expect(product.name).to_be_visible()
    expect(product.price).to_be_visible()
    expect(product.add_to_cart_button).to_be_visible()


@pytest.mark.smoke
@pytest.mark.ui
def test_search_returns_matching_products(page: Page):
    """S06 — Searching 'Hammer' returns relevant results."""
    home = HomePage(page).open()
    home.search("Hammer")
    page.wait_for_selector("a[data-test^='product-']", state="visible", timeout=15_000)
    count = home.get_product_count()
    assert count > 0, "Search for 'Hammer' returned no products"
