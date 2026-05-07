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
    user_page.wait_for_load_state("networkidle")

    # 2. Navigate to checkout and proceed past cart step.
    # Wait for networkidle after goto so the cart component's getCart() API call
    # completes before asserting — proceed-1 is only rendered when cart_items.length > 0.
    user_page.goto(f"{BASE_URL}/checkout")
    user_page.wait_for_load_state("networkidle", timeout=20_000)
    cart = CartPage(user_page)
    expect(cart.proceed_button).to_be_visible()
    cart.proceed_to_checkout()

    # 3. Sign-in step — authenticated users see their account info; click proceed-2 to advance
    checkout = CheckoutPage(user_page)
    expect(checkout.proceed_sign_in).to_be_visible()
    checkout.proceed_from_sign_in()

    # 4. Address step
    expect(checkout.street).to_be_visible()
    checkout.fill_address(DEFAULT_ADDRESS)
    checkout.proceed_from_address()

    # 5. Payment step — Cash on Delivery
    expect(checkout.payment_method).to_be_visible()
    checkout.select_payment_method("Cash on Delivery")
    checkout.finish()

    # 6. Confirmation
    expect(checkout.payment_success).to_be_visible(timeout=10_000)
