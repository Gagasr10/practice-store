from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator("[data-test='product-title']")
        self.proceed_button = page.locator("[data-test='proceed-1']")
        self.cart_total = page.locator("[data-test='cart-total']")

    def open(self) -> "CartPage":
        self.page.goto(f"{BASE_URL}/checkout")
        return self

    def get_item_count(self) -> int:
        return self.items.count()

    def get_total_text(self) -> str:
        return self.cart_total.inner_text()

    def update_quantity(self, item_index: int, qty: int) -> None:
        self.page.locator("[data-test='product-quantity']").nth(item_index).fill(str(qty))

    def remove_item(self, item_index: int) -> None:
        self.page.locator(
            "[data-test^='delete-product-'], a.btn-danger, button.btn-danger"
        ).nth(item_index).click()

    def proceed_to_checkout(self) -> None:
        self.proceed_button.click()
