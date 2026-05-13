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
        # Warm up Angular on the home page first (unguarded) so the auth service has
        # read the token before we hit a protected route — avoids auth-guard race on CI.
        # Use an element wait instead of networkidle; the SPA never reaches networkidle on CI.
        if not self.page.url.startswith(BASE_URL):
            self.page.goto(BASE_URL)
            self.page.wait_for_selector("a[data-test^='product-']", state="visible", timeout=30_000)
        self.page.goto(f"{BASE_URL}/account")
        # Wait for Angular to finish routing — either the account page renders nav-invoices
        # or the auth guard redirects and the login form appears.
        self.page.wait_for_selector(
            "[data-test='nav-invoices'], [data-test='email']",
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
