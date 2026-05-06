from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class ContactPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("[data-test='first-name']")
        self.last_name_input = page.locator("[data-test='last-name']")
        self.email_input = page.locator("[data-test='email']")
        self.subject_select = page.locator("[data-test='subject']")
        self.message_input = page.locator("[data-test='message']")
        self.submit_button = page.locator("[data-test='contact-submit']")
        self.success_message = page.locator("[data-test='contact-succes'], [data-test='contact-success'], .alert-success")

    def open(self) -> "ContactPage":
        self.page.goto(f"{BASE_URL}/contact", wait_until="networkidle")
        return self

    def fill_and_submit(
        self, first_name: str, last_name: str, email: str, subject: str, message: str
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.subject_select.select_option(subject)
        self.message_input.fill(message)
        self.submit_button.click()

    def is_success_visible(self) -> bool:
        return self.success_message.is_visible()
