from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class AccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.invoices_tab = page.locator("[data-test='nav-invoices']")
        self.favourites_tab = page.locator("[data-test='nav-favorites']")
        self.profile_tab = page.locator("[data-test='nav-profile']")
        self.invoice_rows = page.locator("[data-test='invoice-row']")

    def open(self) -> "AccountPage":
        self.page.goto(f"{BASE_URL}/account", wait_until="networkidle")
        return self

    def go_to_orders(self) -> "AccountPage":
        self.invoices_tab.click()
        return self

    def go_to_favourites(self) -> "AccountPage":
        self.favourites_tab.click()
        return self

    def get_invoice_count(self) -> int:
        return self.invoice_rows.count()
