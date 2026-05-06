from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "") -> None:
        self.page.goto(path, wait_until="networkidle")

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url(self, url_pattern: str, timeout: int = 10_000) -> None:
        self.page.wait_for_url(f"**{url_pattern}**", timeout=timeout)

    def toast_success(self) -> Locator:
        return self.page.locator(".toast-success, [data-test='toast-success']")

    def toast_error(self) -> Locator:
        return self.page.locator(".toast-error, [data-test='toast-error']")

    def wait_for_toast(self, timeout: int = 8_000) -> str:
        toast = self.page.locator(".ngx-toastr").first
        toast.wait_for(timeout=timeout)
        return toast.inner_text()
