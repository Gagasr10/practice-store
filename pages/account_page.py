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
        # Navigate to the unguarded home page first so Angular's auth service resolves
        # (getSignedInUser() HTTP call completes) before the protected /account route
        # triggers its auth guard — avoids a redirect-to-login race on slow CI runners.
        self.page.goto(BASE_URL)
        # nav-menu appears only after getSignedInUser() resolves; waiting for it here
        # guarantees auth state is ready before we hit the guarded route.
        self.page.wait_for_selector("[data-test='nav-menu']", state="visible", timeout=30_000)
        self.page.goto(f"{BASE_URL}/account")
        self.page.wait_for_selector("[data-test='nav-menu']", state="visible", timeout=30_000)
        return self

    def go_to_orders(self) -> "AccountPage":
        # nav-invoices lives inside the nav-menu dropdown — open it first
        self.page.locator("[data-test='nav-menu']").click()
        self.invoices_tab.click()
        return self

    def go_to_favourites(self) -> "AccountPage":
        # nav-favorites lives inside the nav-menu dropdown — open it first
        self.page.locator("[data-test='nav-menu']").click()
        self.favourites_tab.click()
        return self

    def get_invoice_count(self) -> int:
        return self.invoice_rows.count()
