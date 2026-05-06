"""R01-R10 — Authentication regression tests."""
import uuid
import pytest
from playwright.sync_api import Page, expect

import api.auth as auth_api
from api.client import ApiClient
from pages.auth_page import AuthPage
from data.test_data import BASE_URL, USER3_EMAIL


@pytest.mark.regression
@pytest.mark.ui
def test_login_wrong_password_shows_error(page: Page):
    # Use USER3 (separate account) to avoid locking the primary USER_EMAIL fixture account
    auth = AuthPage(page).open()
    auth.login(USER3_EMAIL, "totally-wrong-password-xyz")
    expect(auth.error_message).to_be_visible(timeout=6_000)


@pytest.mark.regression
@pytest.mark.ui
def test_login_unknown_email_shows_error(page: Page):
    auth = AuthPage(page).open()
    auth.login("no-such-user@example.com", "password123")
    expect(auth.error_message).to_be_visible(timeout=6_000)


@pytest.mark.regression
@pytest.mark.api
def test_login_locked_account_returns_423():
    # Register a throwaway user, trigger lockout via wrong-password attempts, then verify 423.
    client = ApiClient()
    lock_email = f"lock_{uuid.uuid4().hex[:8]}@example.com"
    lock_pwd = f"Tr3stL0ck_{uuid.uuid4().hex[:8]}!"
    reg = client.post("/users/register", json={
        "first_name": "Lock", "last_name": "Test",
        "email": lock_email, "password": lock_pwd,
        "password_confirmation": lock_pwd,
    })
    if reg.status_code not in (200, 201):
        pytest.skip(f"Could not register throwaway user for lockout test: {reg.text[:100]}")
    # 3 wrong-password attempts lock the account on the 4th
    for _ in range(3):
        client.post("/users/login", json={"email": lock_email, "password": "wrong-password"})
    resp = client.post("/users/login", json={"email": lock_email, "password": "wrong-password"})
    assert resp.status_code == 423


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.xfail(reason="Requires a seeded disabled-account test user", strict=False)
def test_login_disabled_account_returns_403():
    client = ApiClient()
    resp = client.post(
        "/users/login",
        json={"email": "user-disabled@practicesoftwaretesting.com", "password": "welcome01"},
    )
    assert resp.status_code == 403


@pytest.mark.regression
@pytest.mark.ui
def test_register_new_user_can_login(page: Page):
    unique_email = f"reg_{uuid.uuid4().hex[:8]}@example.com"
    unique_pwd = f"Xk9!mPq_{uuid.uuid4().hex[:8]}Z"
    auth = AuthPage(page).open_register()
    auth.register("Test", "Reg", unique_email, unique_pwd)
    page.wait_for_url(lambda url: "/auth/register" not in url, timeout=12_000)
    auth.open()
    auth.login(unique_email, unique_pwd)
    page.wait_for_url(lambda url: "/auth/login" not in url, timeout=8_000)
    assert "/auth/login" not in page.url


@pytest.mark.regression
@pytest.mark.ui
def test_register_duplicate_email_shows_error(page: Page, session_user_email: str, session_user_password: str):
    auth = AuthPage(page).open_register()
    auth.register("Test", "Dup", session_user_email, session_user_password)
    # The app shows field-level errors; look for the email error specifically
    email_error = page.locator("[data-test='email-error'], [id='email-error']")
    general_error = page.locator(".alert-danger")
    # Either an email-specific error or any alert-danger should be visible
    expect(email_error.or_(general_error).first).to_be_visible(timeout=8_000)


@pytest.mark.regression
@pytest.mark.ui
def test_register_weak_password_shows_error(page: Page):
    auth = AuthPage(page).open_register()
    # Fill all required fields but use a weak password (too short)
    auth.first_name_input.fill("Test")
    auth.last_name_input.fill("Weak")
    auth.dob_input.fill("1990-01-01")
    auth.country_select.select_option("US")
    auth.postal_code_input.fill("12345")
    auth.house_number_input.fill("1")
    auth.street_input.fill("Main St")
    auth.city_input.fill("Testville")
    auth.state_input.fill("TX")
    auth.phone_input.fill("5551234567")
    auth.email_input.fill(f"weak_{uuid.uuid4().hex[:8]}@example.com")
    auth.password_input.fill("abc")  # Too short
    auth.register_button.click()
    # Should show a password validation error
    error = page.locator("[data-test='password-error'], .alert-danger")
    expect(error.first).to_be_visible(timeout=6_000)


@pytest.mark.regression
@pytest.mark.ui
def test_change_password_authenticated(browser):
    # Register a throwaway user so shared accounts are not affected
    client = ApiClient()
    throwaway_email = f"chpwd_{uuid.uuid4().hex[:8]}@example.com"
    throwaway_old = f"Xk9!mPq_{uuid.uuid4().hex[:8]}Z"
    throwaway_new = f"Xk9!mPq_{uuid.uuid4().hex[:8]}Z"
    reg = client.post("/users/register", json={
        "first_name": "Change", "last_name": "Pwd",
        "email": throwaway_email, "password": throwaway_old,
        "password_confirmation": throwaway_old,
    })
    if reg.status_code not in (200, 201):
        pytest.skip(f"Could not register throwaway user: {reg.text[:100]}")
    token = auth_api.login(throwaway_email, throwaway_old)["access_token"]

    from data.test_data import AUTH_TOKEN_KEY
    ctx = browser.new_context(base_url=BASE_URL)
    ctx.add_init_script(f"window.localStorage.setItem('{AUTH_TOKEN_KEY}', '{token}')")
    page = ctx.new_page()
    try:
        page.goto(f"{BASE_URL}/account", wait_until="networkidle")
        page.locator("[data-test='nav-profile']").click()
        page.wait_for_load_state("networkidle")
        page.locator("[data-test='current-password']").fill(throwaway_old)
        page.locator("[data-test='new-password']").fill(throwaway_new)
        page.locator("[data-test='new-password-confirm']").fill(throwaway_new)
        page.locator("[data-test='change-password-submit']").click()
        success = page.locator("[role='alert']")
        expect(success.first).to_be_visible(timeout=8_000)
    finally:
        page.close()
        ctx.close()


@pytest.mark.regression
@pytest.mark.api
def test_refresh_token_returns_new_access_token(user_token: str):
    result = auth_api.refresh_token(user_token)
    assert "access_token" in result


@pytest.mark.regression
@pytest.mark.api
def test_forgot_password_accepts_valid_email():
    # Use a throwaway registered user so the forgot-password call (which invalidates
    # the current password) does not corrupt any shared test account.
    client = ApiClient()
    throwaway_email = f"fwdpwd_{uuid.uuid4().hex[:8]}@example.com"
    throwaway_pwd = f"Tr3stFwd_{uuid.uuid4().hex[:8]}!"
    reg = client.post("/users/register", json={
        "first_name": "Fwd", "last_name": "Test",
        "email": throwaway_email, "password": throwaway_pwd,
        "password_confirmation": throwaway_pwd,
    })
    if reg.status_code not in (200, 201):
        pytest.skip(f"Could not register throwaway user: {reg.text[:100]}")
    resp = client.post("/users/forgot-password", json={"email": throwaway_email})
    assert resp.status_code == 200
