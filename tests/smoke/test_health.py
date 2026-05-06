"""S01 — Homepage loads, product grid visible."""
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.ui
def test_homepage_loads_with_products(page: Page):
    home = HomePage(page).open()
    expect(page).to_have_url(f"{home.page.url}")
    expect(home.product_cards.first).to_be_visible()
    assert home.get_product_count() > 0, "No products visible on homepage"
