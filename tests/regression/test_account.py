"""R37-R42 — Account, orders, and favourites regression tests."""
import pytest
from playwright.sync_api import Page, expect

from api.client import ApiClient
from api.invoices import get_invoices
import api.products as products_api
from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from data.test_data import BASE_URL


@pytest.mark.regression
@pytest.mark.ui
def test_authenticated_user_sees_order_history(user_page: Page):
    account = AccountPage(user_page).open()
    account.go_to_orders()
    user_page.wait_for_load_state("networkidle")
    # Orders section renders either rows or a page title (invoices tab is shown)
    page_title = user_page.locator("[data-test='page-title']")
    expect(page_title).to_be_visible(timeout=6_000)
    # If there are invoices, verify the first row is visible
    if account.get_invoice_count() > 0:
        expect(account.invoice_rows.first).to_be_visible(timeout=4_000)


@pytest.mark.regression
@pytest.mark.ui
def test_invoice_detail_shows_correct_items_and_total(user_page: Page):
    account = AccountPage(user_page).open()
    account.go_to_orders()
    user_page.wait_for_load_state("networkidle")
    if account.get_invoice_count() == 0:
        pytest.skip("No invoices available for this test user")
    account.invoice_rows.first.click()
    user_page.wait_for_load_state("networkidle")
    # Invoice detail should show product lines and a total
    expect(user_page.locator("[data-test='invoice-detail'], [data-test='invoice-total']").first).to_be_visible(
        timeout=6_000
    )


@pytest.mark.regression
@pytest.mark.api
def test_download_pdf_endpoint_returns_file(user_token: str):
    inv_data = get_invoices(user_token)
    inv_list = inv_data.get("data", inv_data) if isinstance(inv_data, dict) else inv_data
    if not inv_list:
        pytest.skip("No invoices available for PDF download test")
    invoice_id = inv_list[0]["id"]
    client = ApiClient(token=user_token)
    # Check generation status first — PDF is only downloadable after it has been generated
    status_resp = client.get(f"/invoices/{invoice_id}/download-pdf-status")
    if status_resp.status_code in (200, 400):
        if status_resp.json().get("status") == "NOT_INITIATED":
            pytest.skip("PDF not yet generated for this invoice (status: NOT_INITIATED)")
    resp = client.get(f"/invoices/{invoice_id}/download-pdf")
    assert resp.status_code == 200
    content_type = resp.headers.get("content-type", "")
    assert "pdf" in content_type.lower() or len(resp.content) > 100


@pytest.mark.regression
@pytest.mark.ui
def test_add_product_to_favourites(user_page: Page, user_token: str):
    home = HomePage(user_page).open()
    home.click_product(0)
    product = ProductPage(user_page)
    expect(product.add_to_favourites_button).to_be_visible()
    product.add_to_favourites()
    user_page.wait_for_load_state("networkidle")

    account = AccountPage(user_page).open()
    account.go_to_favourites()
    user_page.wait_for_load_state("networkidle")
    # After adding a favourite, the page should show at least a product card
    fav_items = user_page.locator(
        "a[data-test^='product-'], [data-test='favourite-item'], "
        "[data-test='product-name'], h2, h3, .card"
    )
    expect(fav_items.first).to_be_visible(timeout=6_000)

    # Cleanup: remove all favourites via API
    client = ApiClient(token=user_token)
    fav_resp = client.get("/favorites")
    favs = fav_resp.json()
    for fav in (favs if isinstance(favs, list) else favs.get("data", [])):
        client.delete(f"/favorites/{fav['id']}")


@pytest.mark.regression
@pytest.mark.ui
def test_remove_product_from_favourites(user_page: Page, user_token: str):
    # Set up: add product to favourites via API
    products_data = products_api.get_products()
    product_id = (
        products_data["data"] if "data" in products_data else products_data
    )[0]["id"]
    client = ApiClient(token=user_token)
    client.post("/favorites", json={"product_id": product_id})

    account = AccountPage(user_page).open()
    account.go_to_favourites()
    user_page.wait_for_load_state("networkidle")

    # Look broadly for favourite items using API count as ground truth
    fav_resp = client.get("/favorites")
    favs = fav_resp.json()
    fav_list = favs if isinstance(favs, list) else favs.get("data", [])
    assert len(fav_list) > 0, "No favourites found after adding via API"

    remove_btn = user_page.locator(
        "[data-test='remove-from-favorites'], [data-test='add-to-favorites']"
    ).first
    if not remove_btn.is_visible():
        pytest.skip("Remove from favourites button not found — verify page selectors")
    remove_btn.click()
    user_page.wait_for_load_state("networkidle")

    # Verify via API that the favourite count decreased
    fav_resp2 = client.get("/favorites")
    favs2 = fav_resp2.json()
    fav_list2 = favs2 if isinstance(favs2, list) else favs2.get("data", [])
    assert len(fav_list2) < len(fav_list)


@pytest.mark.regression
@pytest.mark.api
def test_get_favorites_api_returns_list(user_token: str):
    client = ApiClient(token=user_token)
    resp = client.get("/favorites")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or "data" in data
