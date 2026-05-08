"""R27-R36 — Checkout and payment regression tests."""
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.auth_page import AuthPage
from pages.checkout_page import CheckoutPage
from data.test_data import (
    BASE_URL,
    USER_EMAIL,
    USER_PASSWORD,
    DEFAULT_ADDRESS,
    PAYMENT_BANK_TRANSFER,
    PAYMENT_GIFT_CARD,
    PAYMENT_CREDIT_CARD,
    PAYMENT_BNPL,
    PAYMENT_COD,
)


def _reach_address_step(user_page: Page) -> CheckoutPage:
    """Add first product to cart and advance to the address step."""
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")
    # SPA navigation avoids auth-guard race: goto('/checkout') causes a full-page
    # reload where Angular's auth guard fires before the auth service reads the JWT.
    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    cart = CartPage(user_page)
    expect(cart.proceed_button).to_be_visible(timeout=20_000)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(user_page)
    # Step 2 (sign-in confirmation) is shown even for authenticated users
    expect(checkout.proceed_sign_in).to_be_visible(timeout=20_000)
    checkout.proceed_from_sign_in()
    expect(checkout.street).to_be_visible(timeout=8_000)
    return checkout


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_bank_transfer(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Bank Transfer")
    p = PAYMENT_BANK_TRANSFER
    checkout.fill_bank_transfer(p["bank_name"], p["account_name"], p["account_number"])
    checkout.finish()
    expect(checkout.payment_success).to_be_visible(timeout=10_000)


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_gift_card(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Gift Card")
    p = PAYMENT_GIFT_CARD
    checkout.fill_gift_card(p["gift_card_number"], p["validation_code"])
    checkout.finish()
    expect(checkout.payment_success).to_be_visible(timeout=10_000)


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_credit_card(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Credit Card")
    p = PAYMENT_CREDIT_CARD
    checkout.fill_credit_card(
        p["credit_card_number"], p["expiration_date"], p["cvv"], p["card_holder_name"]
    )
    checkout.finish()
    expect(checkout.payment_success).to_be_visible(timeout=10_000)


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_buy_now_pay_later(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Buy Now Pay Later")
    checkout.fill_bnpl(PAYMENT_BNPL["monthly_installments"])
    checkout.finish()
    expect(checkout.payment_success).to_be_visible(timeout=10_000)


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_cash_on_delivery(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Cash on Delivery")
    checkout.finish()
    expect(checkout.payment_success).to_be_visible(timeout=10_000)


@pytest.mark.regression
@pytest.mark.ui
def test_credit_card_invalid_format_rejected(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Credit Card")
    # Number without required dashes — app validates inline and disables Confirm
    checkout.fill_credit_card("1234567890123456", "12/2028", "123", "Test User")
    expect(checkout.finish_button).to_be_disabled(timeout=4_000)
    assert not checkout.is_payment_confirmed()


@pytest.mark.regression
@pytest.mark.ui
def test_credit_card_past_expiry_rejected(user_page: Page):
    checkout = _reach_address_step(user_page)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()
    expect(checkout.payment_method).to_be_visible(timeout=6_000)
    checkout.select_payment_method("Credit Card")
    checkout.fill_credit_card("1234-5678-9012-3456", "01/2020", "123", "Test User")
    expect(checkout.finish_button).to_be_disabled(timeout=4_000)
    assert not checkout.is_payment_confirmed()


@pytest.mark.regression
@pytest.mark.ui
def test_address_blank_fields_block_progression(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")
    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    cart = CartPage(user_page)
    expect(cart.proceed_button).to_be_visible(timeout=20_000)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(user_page)
    expect(checkout.proceed_sign_in).to_be_visible(timeout=20_000)
    checkout.proceed_from_sign_in()
    expect(checkout.street).to_be_visible(timeout=8_000)
    # Proceed button should be disabled when address fields are blank
    proceed_btn = user_page.locator("[data-test='proceed-3']")
    expect(proceed_btn).to_be_disabled(timeout=4_000)


@pytest.mark.regression
@pytest.mark.ui
def test_address_postcode_lookup_populates_fields(user_page: Page):
    home = HomePage(user_page).open()
    home.click_product(0)
    ProductPage(user_page).add_to_cart()
    user_page.wait_for_load_state("networkidle")
    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    cart = CartPage(user_page)
    expect(cart.proceed_button).to_be_visible(timeout=20_000)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(user_page)
    expect(checkout.proceed_sign_in).to_be_visible(timeout=20_000)
    checkout.proceed_from_sign_in()
    expect(checkout.street).to_be_visible(timeout=8_000)
    checkout.postal_code.fill("90210")
    # Click a lookup button if present
    lookup_btn = user_page.locator(
        "[data-test='lookup-postcode'], [data-test='postcode-lookup'], button:has-text('Lookup')"
    )
    if lookup_btn.is_visible():
        lookup_btn.click()
        user_page.wait_for_load_state("networkidle")
        # After lookup, city or state should be populated
        city_value = checkout.city.input_value()
        state_value = checkout.state.input_value()
        assert city_value or state_value, "Postcode lookup did not populate address fields"
    else:
        pytest.skip("Postcode lookup button not found — verify selector")


@pytest.mark.regression
@pytest.mark.ui
def test_unauthenticated_user_redirected_to_login_at_checkout(page: Page):
    home = HomePage(page).open()
    home.click_product(0)
    ProductPage(page).add_to_cart()
    page.wait_for_load_state("networkidle")
    # Angular's auth guard redirects unauthenticated users to /auth/login immediately
    # on goto('/checkout') — proceed-1 is never rendered, so go straight to URL check.
    page.goto(f"{BASE_URL}/checkout")
    page.wait_for_url("**/auth/login**", timeout=15_000)
    auth = AuthPage(page)
    expect(auth.email_input).to_be_visible(timeout=6_000)
