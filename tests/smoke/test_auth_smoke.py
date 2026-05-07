"""S02, S03, S09 — Login (UI + API) and logout."""
import pytest
from playwright.sync_api import Page, expect

import api.auth as auth_api
from data.test_data import BASE_URL
from pages.auth_page import AuthPage
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.api
def test_login_api_returns_bearer_token(session_user_email: str, session_user_password: str):
    """S03 — POST /users/login returns access_token."""
    data = auth_api.login(session_user_email, session_user_password)
    assert "access_token" in data
    assert data.get("token_type", "").lower() == "bearer"


@pytest.mark.smoke
@pytest.mark.ui
def test_login_ui_success(page: Page, session_user_email: str, session_user_password: str):
    """S02 — Login via UI with valid credentials."""
    auth = AuthPage(page).open()
    auth.login(session_user_email, session_user_password)
    # After login the app redirects away from /auth/login
    page.wait_for_url(lambda url: "/auth/login" not in url, timeout=8_000)
    assert "/auth/login" not in page.url


@pytest.mark.smoke
@pytest.mark.ui
def test_logout_clears_session(page: Page, session_user_email: str, session_user_password: str):
    """S09 — Logout redirects user and clears auth state."""
    # Log in first
    auth = AuthPage(page).open()
    auth.login(session_user_email, session_user_password)
    page.wait_for_url(lambda url: "/auth/login" not in url, timeout=8_000)

    # Wait for the auth HTTP call (getSignedInUser → /users/me) to resolve — this
    # is what sets `name` and `role` in the header component, making nav-menu visible.
    page.wait_for_load_state("networkidle", timeout=20_000)
    nav_menu = page.locator("[data-test='nav-menu']")
    expect(nav_menu).to_be_visible(timeout=10_000)
    nav_menu.click()
    page.locator("[data-test='nav-sign-out']").click()

    # Should return to unauthenticated state (login link visible)
    expect(page.locator("[data-test='nav-sign-in']")).to_be_visible(timeout=6_000)
