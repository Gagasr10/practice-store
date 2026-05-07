from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.locator("[data-test='product-name']")
        self.price = page.locator("[data-test='unit-price']")
        self.description = page.locator("[data-test='product-description']")
        self.quantity_input = page.locator("[data-test='quantity']")
        self.add_to_cart_button = page.locator("[data-test='add-to-cart']")
        self.add_to_favourites_button = page.locator("[data-test='add-to-favorites']")
        self.related_products = page.locator("[data-test='related-product']")

    def get_name(self) -> str:
        return self.name.inner_text()

    def get_price(self) -> str:
        return self.price.inner_text()

    def set_quantity(self, qty: int) -> None:
        self.quantity_input.fill(str(qty))

    def add_to_cart(self) -> None:
        expect(self.add_to_cart_button).to_be_visible(timeout=15_000)
        expect(self.add_to_cart_button).to_be_enabled(timeout=30_000)
        self.add_to_cart_button.click()

    def add_to_favourites(self) -> None:
        expect(self.add_to_favourites_button).to_be_visible(timeout=15_000)
        expect(self.add_to_favourites_button).to_be_enabled(timeout=30_000)
        self.add_to_favourites_button.click()

    def get_related_product_count(self) -> int:
        return self.related_products.count()
