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
        # Land on the unguarded home page so Angular's auth service resolves
        # (getSignedInUser() completes) without triggering the /account route guard.
        # All callers follow open() with go_to_orders() or go_to_favourites(), which
        # do SPA navigation via the nav-menu dropdown — no second full page load needed.
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        # nav-menu appears only after getSignedInUser() resolves. 60s budget covers
        # slow CI runners hitting the external API.
        self.page.wait_for_selector("[data-test='nav-menu']", state="visible", timeout=60_000)
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
