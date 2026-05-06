from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from data.test_data import BASE_URL


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_cards = page.locator("a[data-test^='product-']")
        self.search_input = page.locator("[data-test='search-query']")
        self.search_button = page.locator("[data-test='search-submit']")
        self.nav_sign_in = page.locator("[data-test='nav-sign-in']")
        self.nav_cart = page.locator("[data-test='nav-cart']")
        self.sort_select = page.locator("[data-test='sort']")
        self.category_links = page.locator(
            "[data-test='nav-hand-tools'], [data-test='nav-power-tools'], "
            "[data-test='nav-other'], [data-test='nav-special-tools'], [data-test='nav-rentals']"
        )

    def open(self) -> "HomePage":
        self.page.goto(BASE_URL)
        return self

    def search(self, keyword: str) -> "HomePage":
        self.search_input.fill(keyword)
        self.search_button.click()
        return self

    def get_product_count(self) -> int:
        return self.product_cards.count()

    def click_product(self, index: int = 0) -> None:
        self.product_cards.nth(index).click()

    def click_sign_in(self) -> None:
        self.nav_sign_in.click()

    def click_cart(self) -> None:
        self.nav_cart.click()

    def filter_by_category(self, name: str) -> "HomePage":
        self.page.locator("label", has_text=name).click()
        return self
