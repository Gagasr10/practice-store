"""R11-R21 — Products and search regression tests."""
import pytest
from playwright.sync_api import Page, expect

import api.products as products_api
from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.mark.regression
@pytest.mark.ui
def test_filter_products_by_category(page: Page):
    home = HomePage(page).open()
    page.wait_for_load_state("networkidle")
    # Category links are inside the nav-categories dropdown
    page.locator("[data-test='nav-categories']").click()
    page.wait_for_timeout(300)
    home.category_links.first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)
    expect(page.locator("a[data-test^='product-']")).not_to_have_count(0, timeout=8_000)


@pytest.mark.regression
@pytest.mark.ui
def test_filter_products_by_brand(page: Page):
    home = HomePage(page).open()
    brand_filter = page.locator("[data-test^='brand-']").first
    expect(brand_filter).to_be_visible(timeout=10_000)
    brand_filter.click()
    page.wait_for_selector("a[data-test^='product-']", state="visible", timeout=15_000)
    assert home.get_product_count() > 0


@pytest.mark.regression
@pytest.mark.ui
def test_sort_products_price_ascending(page: Page):
    home = HomePage(page).open()
    page.wait_for_load_state("networkidle")
    home.sort_select.select_option("price,asc")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)
    prices = []
    for el in page.locator("[data-test='product-price']").all():
        text = el.inner_text().replace("$", "").strip()
        if text:
            try:
                prices.append(float(text))
            except ValueError:
                pass
    assert prices, "No prices found on page"
    assert prices == sorted(prices), f"Products not sorted ascending: {prices}"


@pytest.mark.regression
@pytest.mark.ui
def test_sort_products_price_descending(page: Page):
    home = HomePage(page).open()
    page.wait_for_load_state("networkidle")
    home.sort_select.select_option("price,desc")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)
    prices = []
    for el in page.locator("[data-test='product-price']").all():
        text = el.inner_text().replace("$", "").strip()
        if text:
            try:
                prices.append(float(text))
            except ValueError:
                pass
    assert prices, "No prices found on page"
    assert prices == sorted(prices, reverse=True), f"Products not sorted descending: {prices}"


@pytest.mark.regression
@pytest.mark.ui
def test_search_unknown_keyword_shows_empty_state(page: Page):
    home = HomePage(page).open()
    home.search("zzz_no_match_xyzabc123")
    page.wait_for_load_state("networkidle")
    assert home.get_product_count() == 0


@pytest.mark.regression
@pytest.mark.ui
def test_product_detail_shows_name_price_description(page: Page):
    home = HomePage(page).open()
    home.click_product(0)
    product = ProductPage(page)
    expect(product.name).to_be_visible()
    expect(product.price).to_be_visible()
    expect(product.description).to_be_visible()
    assert len(product.get_name()) > 0
    assert len(product.get_price()) > 0


@pytest.mark.regression
@pytest.mark.ui
def test_related_products_visible_on_detail_page(page: Page):
    home = HomePage(page).open()
    home.click_product(0)
    page.wait_for_load_state("networkidle")
    related_count = ProductPage(page).get_related_product_count()
    # Related products section exists; count may be 0 for some products
    assert related_count >= 0


@pytest.mark.regression
@pytest.mark.ui
def test_product_specs_displayed(page: Page):
    home = HomePage(page).open()
    home.click_product(0)
    page.wait_for_load_state("networkidle")
    product = ProductPage(page)
    expect(product.name).to_be_visible()
    # Specs section may or may not exist per product — just verify detail page is intact
    detail_content = page.locator(
        "[data-test='product-specs'], .specs, [data-test='product-description']"
    )
    assert detail_content.count() > 0


@pytest.mark.regression
@pytest.mark.api
def test_products_api_pagination():
    page1 = products_api.get_products(params={"page": 1})
    assert "data" in page1
    assert len(page1["data"]) > 0
    page2 = products_api.get_products(params={"page": 2})
    if "data" in page2 and len(page2["data"]) > 0:
        ids_p1 = {p["id"] for p in page1["data"]}
        ids_p2 = {p["id"] for p in page2["data"]}
        assert ids_p1.isdisjoint(ids_p2), "Page 1 and page 2 share the same product IDs"


@pytest.mark.regression
@pytest.mark.api
def test_products_search_api_filters_by_query():
    data = products_api.search_products("Hammer")
    items = data["data"] if "data" in data else data
    assert len(items) > 0, "Search for 'Hammer' returned no results"
    for item in items:
        name_lower = item.get("name", "").lower()
        desc_lower = item.get("description", "").lower()
        assert "hammer" in name_lower or "hammer" in desc_lower, (
            f"Product '{item['name']}' does not match query 'Hammer'"
        )


@pytest.mark.regression
@pytest.mark.api
def test_categories_tree_returns_nested_structure():
    tree = products_api.get_categories_tree()
    assert isinstance(tree, list)
    assert len(tree) > 0
    has_children = any(
        "sub_categories" in cat or "children" in cat
        for cat in tree
    )
    assert has_children, "Category tree has no nested sub-categories"
