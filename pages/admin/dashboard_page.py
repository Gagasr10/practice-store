from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class AdminDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.products_nav = page.locator("[data-test='nav-admin-products']")
        self.categories_nav = page.locator("[data-test='nav-admin-categories']")
        self.brands_nav = page.locator("[data-test='nav-admin-brands']")
        self.users_nav = page.locator("[data-test='nav-admin-users']")
        self.invoices_nav = page.locator("[data-test='nav-admin-orders']")
        self.reports_nav = page.locator("[data-test='nav-admin-statistics']")

    def open(self) -> "AdminDashboardPage":
        self.page.goto(f"{BASE_URL}/admin")
        # nav-admin-* links live inside the hamburger dropdown and are never visible
        # until opened — wait for nav-menu (the toggle button) instead
        self.page.wait_for_selector("[data-test='nav-menu']", state="visible", timeout=30_000)
        return self

    def go_to_products(self) -> None:
        self.products_nav.click()

    def go_to_invoices(self) -> None:
        self.invoices_nav.click()

    def go_to_users(self) -> None:
        self.users_nav.click()

    def go_to_reports(self) -> None:
        self.reports_nav.click()

    def is_dashboard_visible(self) -> bool:
        return self.page.url.endswith("/admin") or "/admin" in self.page.url
