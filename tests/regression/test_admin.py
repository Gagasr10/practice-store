"""R46-R54 — Admin regression tests."""
import uuid
import pytest
from playwright.sync_api import Page, expect

from api.client import ApiClient
import api.products as products_api
from api.invoices import get_invoices, update_invoice_status
from pages.admin.dashboard_page import AdminDashboardPage
from pages.admin.products_page import AdminProductsPage
from data.test_data import BASE_URL, ADMIN_EMAIL


def _get_first_category_and_brand(admin_token: str):
    """Return (category_id, brand_id, product_image_id) from the first available items."""
    cats = products_api.get_categories()
    cat_list = cats if isinstance(cats, list) else cats.get("data", [])
    category_id = cat_list[0]["id"]

    client = ApiClient(token=admin_token)
    brands_resp = client.get("/brands")
    brands = brands_resp.json()
    brand_list = brands if isinstance(brands, list) else brands.get("data", [])
    brand_id = brand_list[0]["id"]

    # Get a valid product_image_id from an existing product
    existing = products_api.get_products()
    existing_list = existing["data"] if "data" in existing else existing
    product_image_id = existing_list[0].get("product_image", {}).get("id", "")

    return category_id, brand_id, product_image_id


@pytest.mark.regression
@pytest.mark.ui
def test_admin_creates_product(admin_page: Page, admin_token: str):
    unique_name = f"Test Tool {uuid.uuid4().hex[:6]}"
    category_id, brand_id, product_image_id = _get_first_category_and_brand(admin_token)

    products_page = AdminProductsPage(admin_page).open()
    admin_page.wait_for_load_state("networkidle")
    products_page.click_add_new()
    admin_page.wait_for_load_state("networkidle")

    products_page.fill_product_form(unique_name, "19.99", "25")
    admin_page.locator("[data-test='brand-id']").select_option(brand_id)
    admin_page.locator("[data-test='category-id']").select_option(category_id)
    if product_image_id:
        admin_page.locator("[data-test='product-image-id']").select_option(product_image_id)
    products_page.save()
    admin_page.wait_for_load_state("networkidle")

    success = admin_page.locator(
        "[data-test='toast-success'], .alert-success, [data-test='alert-success']"
    )
    expect(success).to_be_visible(timeout=6_000)

    # Cleanup: delete the created product via API
    data = products_api.get_products()
    items = data["data"] if "data" in data else data
    created = next((p for p in items if p["name"] == unique_name), None)
    if created:
        products_api.delete_product(created["id"], admin_token)


@pytest.mark.regression
@pytest.mark.ui
def test_admin_edits_product(admin_page: Page, admin_token: str):
    category_id, brand_id, product_image_id = _get_first_category_and_brand(admin_token)
    original_name = f"EditMe {uuid.uuid4().hex[:6]}"
    updated_name = f"Edited {uuid.uuid4().hex[:6]}"

    product = products_api.create_product(
        {
            "name": original_name,
            "description": "Temporary test product",
            "price": 9.99,
            "stock": 5,
            "is_rental": False,
            "is_location_offer": False,
            "category_id": category_id,
            "brand_id": brand_id,
            "product_image_id": product_image_id,
        },
        admin_token,
    )
    product_id = product["id"]

    try:
        # Navigate to the edit page
        admin_page.goto(f"{BASE_URL}/admin/products/edit/{product_id}")
        admin_page.wait_for_load_state("networkidle")

        name_field = admin_page.locator("[data-test='name']")
        expect(name_field).to_be_visible(timeout=6_000)
        name_field.clear()
        name_field.fill(updated_name)

        # Angular doesn't pre-populate dropdowns/stock on the edit form; fill all required fields
        stock_field = admin_page.locator("[data-test='stock']")
        stock_field.clear()
        stock_field.fill("5")
        admin_page.locator("[data-test='brand-id']").select_option(brand_id)
        admin_page.locator("[data-test='category-id']").select_option(category_id)
        if product_image_id:
            admin_page.locator("[data-test='product-image-id']").select_option(product_image_id)

        admin_page.locator("[data-test='product-submit']").click()
        admin_page.wait_for_load_state("networkidle")
        success = admin_page.locator(
            "[role='alert'], [data-test='toast-success'], .alert-success"
        )
        expect(success.first).to_be_visible(timeout=6_000)

        # Verify via API
        updated = products_api.get_product(product_id)
        assert updated["name"] == updated_name
    finally:
        products_api.delete_product(product_id, admin_token)


@pytest.mark.regression
@pytest.mark.ui
def test_admin_deletes_product(admin_page: Page, admin_token: str):
    category_id, brand_id, product_image_id = _get_first_category_and_brand(admin_token)
    test_name = f"DeleteMe {uuid.uuid4().hex[:6]}"

    product = products_api.create_product(
        {
            "name": test_name,
            "description": "Temporary test product for deletion",
            "price": 4.99,
            "stock": 1,
            "is_rental": False,
            "is_location_offer": False,
            "category_id": category_id,
            "brand_id": brand_id,
            "product_image_id": product_image_id,
        },
        admin_token,
    )
    product_id = product["id"]

    products_page = AdminProductsPage(admin_page).open()
    admin_page.wait_for_load_state("networkidle")
    # Search for the product by name so pagination doesn't hide it
    search_input = admin_page.locator("[data-test='product-search-query']")
    search_input.fill(test_name)
    admin_page.locator("[data-test='product-search-submit']").click()
    admin_page.wait_for_load_state("networkidle")
    admin_page.wait_for_timeout(800)
    delete_btn = admin_page.locator(f"[data-test='product-delete-{product_id}']")
    expect(delete_btn).to_be_visible(timeout=8_000)
    delete_btn.click()
    # Handle optional confirmation dialog
    confirm = admin_page.locator(
        "[data-test='confirm-btn'], button:has-text('Yes'), .btn-danger:has-text('OK')"
    )
    try:
        confirm.first.click(timeout=2_000)
    except Exception:
        pass
    admin_page.wait_for_load_state("networkidle")

    # Verify gone via API (404 expected)
    client = ApiClient(token=admin_token)
    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 404


@pytest.mark.regression
@pytest.mark.api
def test_admin_creates_category(admin_token: str):
    client = ApiClient(token=admin_token)
    slug = f"test-cat-{uuid.uuid4().hex[:6]}"
    resp = client.post("/categories", json={"name": f"Test Category {slug}", "slug": slug})
    assert resp.status_code in (200, 201)
    cat_id = resp.json()["id"]
    client.delete(f"/categories/{cat_id}")


@pytest.mark.regression
@pytest.mark.api
def test_admin_creates_brand(admin_token: str):
    client = ApiClient(token=admin_token)
    slug = f"test-brand-{uuid.uuid4().hex[:6]}"
    resp = client.post("/brands", json={"name": f"Test Brand {slug}", "slug": slug})
    assert resp.status_code in (200, 201)
    brand_id = resp.json()["id"]
    client.delete(f"/brands/{brand_id}")


@pytest.mark.regression
@pytest.mark.api
def test_admin_updates_invoice_status(admin_token: str):
    client = ApiClient(token=admin_token)
    resp = client.get("/invoices")
    inv_data = resp.json()
    invoices = inv_data.get("data", inv_data) if isinstance(inv_data, dict) else inv_data
    if not invoices:
        pytest.skip("No invoices available to update status")
    invoice_id = invoices[0]["id"]
    original_status = invoices[0]["status"]
    # COMPLETED only accepts ON_HOLD/AWAITING_FULFILLMENT/SHIPPED — not PENDING
    new_status = "ON_HOLD" if original_status == "COMPLETED" else "COMPLETED"

    update_invoice_status(invoice_id, new_status, admin_token)
    # Verify via a GET (the PUT response only returns {'success': True})
    updated = client.get(f"/invoices/{invoice_id}").json()
    assert updated.get("status") == new_status

    # Revert
    update_invoice_status(invoice_id, original_status, admin_token)


@pytest.mark.regression
@pytest.mark.ui
def test_admin_views_user_list(admin_page: Page):
    AdminDashboardPage(admin_page).open()
    admin_page.wait_for_load_state("networkidle")
    # Admin nav links are inside the hamburger menu — open it first
    admin_page.locator("[data-test='nav-menu']").click()
    admin_page.wait_for_timeout(300)
    admin_page.locator("[data-test='nav-admin-users']").click()
    admin_page.wait_for_load_state("networkidle")
    user_rows = admin_page.locator("[data-test='user-row'], tr:has-text('@')")
    expect(user_rows.first).to_be_visible(timeout=6_000)


@pytest.mark.regression
@pytest.mark.api
def test_get_top10_products_report_with_admin_token(admin_token: str):
    client = ApiClient(token=admin_token)
    resp = client.get("/reports/top10-purchased-products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or "data" in data


@pytest.mark.regression
@pytest.mark.api
def test_non_admin_token_rejected_on_admin_endpoints(user_token: str):
    client = ApiClient(token=user_token)
    resp = client.get("/reports/top10-purchased-products")
    assert resp.status_code == 403
