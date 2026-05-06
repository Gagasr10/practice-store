"""R43-R45 — Contact form regression tests."""
import pytest
from playwright.sync_api import Page, expect

from api.client import ApiClient
from pages.contact_page import ContactPage


@pytest.mark.regression
@pytest.mark.ui
def test_contact_form_submits_successfully(page: Page):
    contact = ContactPage(page).open()
    contact.fill_and_submit(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        subject="customer-service",
        message="This is an automated test message for QA. Please ignore.",
    )
    expect(page.locator("[data-test='contact-succes'], [data-test='contact-success'], .alert-success")).to_be_visible(
        timeout=6_000
    )


@pytest.mark.regression
@pytest.mark.ui
def test_contact_form_empty_fields_blocked(page: Page):
    contact = ContactPage(page).open()
    contact.submit_button.click()
    assert not contact.is_success_visible()
    error = page.locator(".invalid-feedback, [data-test='error-msg'], .alert-danger")
    expect(error.first).to_be_visible(timeout=4_000)


@pytest.mark.regression
@pytest.mark.api
def test_post_messages_creates_record():
    client = ApiClient()
    payload = {
        "name": "API Test User",
        "email": "api-test@example.com",
        "subject": "API Test Subject",
        "message": "This is an automated API test message.",
    }
    resp = client.post("/messages", json=payload)
    assert resp.status_code in (200, 201)
