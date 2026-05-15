"""S08 — Full checkout happy path with Cash on Delivery."""
import pytest
from playwright.sync_api import Page, expect

from data.test_data import BASE_URL, DEFAULT_ADDRESS
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.smoke
@pytest.mark.ui
def test_full_checkout_cash_on_delivery(user_page: Page):
    """S08 — End-to-end checkout (authenticated): browse → cart → address → COD → confirm."""
    # 1. Add a product to cart
    home = HomePage(user_page).open()
    home.click_product(0)
    product = ProductPage(user_page)
    expect(product.add_to_cart_button).to_be_visible()
    product.add_to_cart()
    user_page.wait_for_selector("[data-test='nav-cart']", state="visible", timeout=15_000)

    # 2. Navigate to checkout via the nav-cart link (SPA navigation).
    # Avoid goto('/checkout') which causes a full-page reload: Angular re-bootstraps
    # and the checkout route's auth guard can fire before the auth service has read
    # the JWT from localStorage, redirecting back to login and leaving an empty cart.
    # Clicking nav-cart is a client-side router navigation on an already-initialised
    # Angular app, so auth state and sessionStorage cart_id are preserved.
    user_page.locator("[data-test='nav-cart']").click()
    user_page.wait_for_url("**/checkout**", timeout=10_000)
    cart = CartPage(user_page)
    expect(cart.proceed_button).to_be_visible(timeout=20_000)
    cart.proceed_to_checkout()

    # 3. Step 2 (sign-in): authenticated users still land here — click Proceed
    checkout = CheckoutPage(user_page)
    expect(checkout.proceed_sign_in).to_be_visible(timeout=15_000)
    checkout.proceed_from_sign_in()
    # 4. Billing address (step 3)
    expect(checkout.country).to_be_visible(timeout=15_000)
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()

    # 4. Payment step — Cash on Delivery
    expect(checkout.payment_method).to_be_visible()
    checkout.select_payment_method("Cash on Delivery")
    checkout.finish()

    # 5. Confirmation
    expect(checkout.payment_success).to_be_visible(timeout=10_000)
