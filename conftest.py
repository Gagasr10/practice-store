import time
import uuid
import requests
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect as pw_expect

import api.auth as auth_api
from api.client import ApiClient
from data.test_data import (
    API_BASE_URL,
    AUTH_TOKEN_KEY,
    BASE_URL,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    USER_EMAIL,
    USER_PASSWORD,
    USER3_EMAIL,
    USER3_PASSWORD,
)


# ---------------------------------------------------------------------------
# Global Playwright defaults — applied once per session
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def configure_playwright_defaults():
    """Raise assertion timeout from 5s to 15s to give Angular time to render on CI."""
    pw_expect.set_options(timeout=15_000)


# ---------------------------------------------------------------------------
# Session-level DB reset — runs once per test run before anything else
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    """Reset the shared practice-store database and wait until products are seeded."""
    requests.post(f"{API_BASE_URL}/refresh", timeout=30)
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            r = requests.get(f"{API_BASE_URL}/products", timeout=10)
            if r.status_code == 200:
                body = r.json()
                items = body.get("data", body) if isinstance(body, dict) else body
                if isinstance(items, list) and len(items) > 0:
                    return
        except Exception:
            pass
        time.sleep(3)


# ---------------------------------------------------------------------------
# Session-level user credential resolver
#
# The practice store is a shared environment — seeded accounts can be locked
# or have their passwords changed by other users at any time.  This fixture
# tries the known accounts in priority order; if all are unavailable it
# registers a throwaway user for the current test session.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def session_user_creds() -> tuple[str, str]:
    """Return (email, password) for a working customer account."""
    for email, pwd in [(USER_EMAIL, USER_PASSWORD), (USER3_EMAIL, USER3_PASSWORD)]:
        try:
            auth_api.login(email, pwd)
            return email, pwd
        except Exception:
            continue

    # All seeded accounts are broken — register a throwaway user for this session
    client = ApiClient()
    fresh_email = f"sesstest_{uuid.uuid4().hex[:8]}@example.com"
    fresh_pwd = f"SessT3st_{uuid.uuid4().hex[:8]}!"
    reg = client.post("/users/register", json={
        "first_name": "Session", "last_name": "Tester",
        "email": fresh_email, "password": fresh_pwd,
        "password_confirmation": fresh_pwd,
    })
    if reg.status_code in (200, 201):
        return fresh_email, fresh_pwd

    return None, None


@pytest.fixture(scope="session")
def session_user_email(session_user_creds) -> str:
    """Email of the effective test user for this session."""
    email, _ = session_user_creds
    if not email:
        pytest.skip("No working user account available in shared environment")
    return email


@pytest.fixture(scope="session")
def session_user_password(session_user_creds) -> str:
    """Password of the effective test user for this session."""
    _, pwd = session_user_creds
    if not pwd:
        pytest.skip("No working user account available in shared environment")
    return pwd


# ---------------------------------------------------------------------------
# API auth fixtures (no browser, fast)
# ---------------------------------------------------------------------------

@pytest.fixture
def user_token(session_user_creds) -> str:
    email, pwd = session_user_creds
    if not email:
        pytest.skip("User credentials unavailable in shared environment")
    try:
        return auth_api.login(email, pwd)["access_token"]
    except Exception as exc:
        pytest.skip(f"User login failed: {exc}")


@pytest.fixture
def admin_token() -> str:
    try:
        return auth_api.login(ADMIN_EMAIL, ADMIN_PASSWORD)["access_token"]
    except Exception as exc:
        pytest.skip(f"Admin credentials unavailable in shared environment: {exc}")


# ---------------------------------------------------------------------------
# UI auth fixtures — inject token into localStorage before each test
# ---------------------------------------------------------------------------

@pytest.fixture
def user_context(browser: Browser, user_token: str) -> BrowserContext:
    """Browser context with the customer JWT pre-loaded into localStorage."""
    context = browser.new_context(base_url=BASE_URL)
    context.add_init_script(
        f"window.localStorage.setItem('{AUTH_TOKEN_KEY}', '{user_token}')"
    )
    yield context
    context.close()


@pytest.fixture
def admin_context(browser: Browser, admin_token: str) -> BrowserContext:
    """Browser context with the admin JWT pre-loaded into localStorage."""
    context = browser.new_context(base_url=BASE_URL)
    context.add_init_script(
        f"window.localStorage.setItem('{AUTH_TOKEN_KEY}', '{admin_token}')"
    )
    yield context
    context.close()


@pytest.fixture
def user_page(user_context: BrowserContext) -> Page:
    """Authenticated page for customer tests."""
    page = user_context.new_page()
    yield page
    page.close()


@pytest.fixture
def admin_page(admin_context: BrowserContext) -> Page:
    """Authenticated page for admin tests."""
    page = admin_context.new_page()
    yield page
    page.close()
