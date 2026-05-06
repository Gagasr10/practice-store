from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class AdminProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_new_button = page.locator("[data-test='product-add']")
        self.save_button = page.locator("[data-test='product-submit']")
        self.product_rows = page.locator("[data-test^='product-edit-']")

        # Product form fields
        self.name_input = page.locator("[data-test='name']")
        self.price_input = page.locator("[data-test='price']")
        self.stock_input = page.locator("[data-test='stock']")
        self.description_input = page.locator("[data-test='description']")
        self.brand_select = page.locator("[data-test='brand-id']")
        self.category_select = page.locator("[data-test='category-id']")

    def open(self) -> "AdminProductsPage":
        self.page.goto(f"{BASE_URL}/admin/products")
        return self

    def click_add_new(self) -> None:
        self.add_new_button.click()

    def fill_product_form(self, name: str, price: str, stock: str, description: str = "Test product description") -> None:
        self.name_input.fill(name)
        self.price_input.fill(price)
        self.stock_input.fill(stock)
        self.description_input.fill(description)

    def save(self) -> None:
        self.save_button.click()

    def get_edit_link(self, product_id: str):
        return self.page.locator(f"[data-test='product-edit-{product_id}']")

    def get_delete_button(self, product_id: str):
        return self.page.locator(f"[data-test='product-delete-{product_id}']")
