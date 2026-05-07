"""S02, S03, S09 — Login (UI + API) and logout."""
import pytest
from playwright.sync_api import Page, expect

import api.auth as auth_api
from data.test_data import BASE_URL
from pages.auth_page import AuthPage


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
def test_logout_clears_session(user_page: Page):
    """S09 — Logout redirects user and clears auth state."""
    # Use the pre-authenticated user_page (JWT injected via add_init_script into
    # localStorage before Angular bootstraps). Navigate to the unguarded home page
    # so the auth service initialises before any route guard runs — avoids the
    # race where goto('/account') triggers an auth-guard redirect back to login.
    user_page.goto(BASE_URL)

    # nav-menu appears after Angular's getSignedInUser() HTTP call sets name/role
    nav_menu = user_page.locator("[data-test='nav-menu']")
    expect(nav_menu).to_be_visible(timeout=20_000)
    nav_menu.click()
    user_page.locator("[data-test='nav-sign-out']").click()

    # After logout Angular removes nav-menu from the DOM (@if(name && role) → false).
    # Don't assert nav-sign-in: the app redirects to /auth/login where that link is
    # intentionally hidden (you are already on the sign-in page).
    expect(user_page.locator("[data-test='nav-menu']")).to_be_hidden(timeout=10_000)
