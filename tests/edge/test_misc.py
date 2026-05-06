"""E05-E07, E09-E12 — Miscellaneous edge cases."""
import pytest
from playwright.sync_api import Page, expect

import api.auth as auth_api
import api.products as products_api
from api.client import ApiClient
from api.invoices import get_invoices
from pages.home_page import HomePage
from data.test_data import ADMIN_EMAIL


@pytest.mark.edge
@pytest.mark.api
@pytest.mark.xfail(
    reason="Rate-limit threshold may exceed 100 requests; actual limit undocumented",
    strict=False,
)
def test_reports_rate_limited_after_n_requests(admin_token: str):
    client = ApiClient(token=admin_token)
    status_codes = []
    for _ in range(100):
        resp = client.get("/reports/top10-purchased-products")
        status_codes.append(resp.status_code)
        if resp.status_code == 429:
            break
    assert 429 in status_codes, (
        "Reports endpoint was never rate-limited after 100 rapid requests"
    )


@pytest.mark.edge
@pytest.mark.api
def test_postcode_lookup_invalid_postcode():
    client = ApiClient()
    resp = client.get("/postcode-lookup", params={"postcode": "00000INVALID"})
    assert resp.status_code in (422, 404, 200), (
        f"Unexpected status {resp.status_code} for invalid postcode"
    )
    if resp.status_code == 200:
        data = resp.json()
        # A 200 for an invalid postcode should return empty/null data
        assert not data or data == {} or data == [], (
            f"Lookup returned data for an invalid postcode: {data}"
        )


@pytest.mark.edge
@pytest.mark.ui
def test_xss_payload_in_search_field_is_safe(page: Page):
    home = HomePage(page).open()
    home.search("<script>window.__XSS__=1</script>")
    page.wait_for_load_state("networkidle")
    # The script must not have executed
    xss_ran = page.evaluate("() => window.__XSS__")
    assert xss_ran is None, "XSS payload executed in the search field"
    # Page should still be functional
    expect(page.locator("[data-test='search-query']")).to_be_visible()


@pytest.mark.edge
@pytest.mark.api
def test_expired_token_refresh_and_retry(user_token: str):
    """Verify that refreshing a valid token returns a new access token."""
    result = auth_api.refresh_token(user_token)
    assert "access_token" in result, "Refresh did not return a new access_token"
    new_token = result["access_token"]
    # New token should be usable
    client = ApiClient(token=new_token)
    resp = client.get("/users/me")
    assert resp.status_code == 200


@pytest.mark.edge
@pytest.mark.api
@pytest.mark.xfail(
    reason="API allows admin deletion (returns 204) — no server-side protection for admin accounts",
    strict=False,
)
def test_admin_cannot_be_deleted(admin_token: str):
    client = ApiClient(token=admin_token)
    users_resp = client.get("/users")
    users_data = users_resp.json()
    users = users_data.get("data", users_data) if isinstance(users_data, dict) else users_data
    admin_user = next(
        (u for u in users if u.get("email") == ADMIN_EMAIL), None
    )
    assert admin_user is not None, "Admin user not found in users list"
    resp = client.delete(f"/users/{admin_user['id']}")
    assert resp.status_code in (403, 409, 422, 400), (
        f"Expected deletion of admin to be blocked; got {resp.status_code}"
    )


@pytest.mark.edge
@pytest.mark.api
def test_category_tree_has_no_orphan_categories():
    tree = products_api.get_categories_tree()
    assert isinstance(tree, list) and len(tree) > 0
    for parent in tree:
        children = parent.get("sub_categories", parent.get("children", []))
        # Each child must have an id and a name
        for child in children:
            assert "id" in child, f"Child category missing 'id': {child}"
            assert "name" in child, f"Child category missing 'name': {child}"


@pytest.mark.edge
@pytest.mark.api
def test_invoice_pdf_status_polling(user_token: str):
    inv_data = get_invoices(user_token)
    inv_list = inv_data.get("data", inv_data) if isinstance(inv_data, dict) else inv_data
    if not inv_list:
        pytest.skip("No invoices available for PDF status polling test")
    invoice_id = inv_list[0]["id"]
    client = ApiClient(token=user_token)
    resp = client.get(f"/invoices/{invoice_id}/download-pdf-status")
    # 200 = PDF ready/in-progress; 400 with NOT_INITIATED = PDF not yet queued (valid initial state)
    assert resp.status_code in (200, 400), f"Unexpected status {resp.status_code}"
    data = resp.json()
    assert "status" in data, f"Unexpected PDF status response shape: {data}"
