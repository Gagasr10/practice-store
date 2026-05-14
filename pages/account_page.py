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
        # Always warm up Angular on the home page first so the auth service has read
        # the token before hitting the protected /account route.
        self.page.goto(BASE_URL)
        self.page.wait_for_selector("a[data-test^='product-']", state="visible", timeout=30_000)
        self.page.goto(f"{BASE_URL}/account")
        # Wait for Angular to finish routing. nav-invoices is the account nav tab;
        # nav-menu is the authenticated-user dropdown in the main nav (appears as soon
        # as the auth service resolves, before account data finishes loading);
        # email is shown if the auth guard redirects to the login page.
        self.page.wait_for_selector(
            "[data-test='nav-invoices'], [data-test='nav-menu'], [data-test='email']",
            state="visible",
            timeout=30_000,
        )
        if "/auth/login" in self.page.url:
            self.page.goto(f"{BASE_URL}/account")
            self.page.wait_for_selector("[data-test='nav-invoices']", state="visible", timeout=30_000)
        return self

    def go_to_orders(self) -> "AccountPage":
        self.invoices_tab.click()
        return self

    def go_to_favourites(self) -> "AccountPage":
        self.favourites_tab.click()
        return self

    def get_invoice_count(self) -> int:
        return self.invoice_rows.count()
