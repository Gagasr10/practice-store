from playwright.sync_api import Page
from pages.base_page import BasePage
from data.test_data import BASE_URL


class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("[data-test='email']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-submit']")
        self.register_link = page.locator("[data-test='register-link']")
        self.forgot_password_link = page.locator("[data-test='forgot-password-link']")
        self.error_message = page.locator("[data-test='login-error']")

        # Registration fields
        self.first_name_input = page.locator("[data-test='first-name']")
        self.last_name_input = page.locator("[data-test='last-name']")
        self.dob_input = page.locator("[data-test='dob']")
        self.country_select = page.locator("[data-test='country']")
        self.postal_code_input = page.locator("[data-test='postal_code']")
        self.house_number_input = page.locator("[data-test='house_number']")
        self.street_input = page.locator("[data-test='street']")
        self.city_input = page.locator("[data-test='city']")
        self.state_input = page.locator("[data-test='state']")
        self.phone_input = page.locator("[data-test='phone']")
        self.register_button = page.locator("[data-test='register-submit']")
        self.register_error = page.locator("[data-test='register-error']")

    def open(self) -> "AuthPage":
        self.page.goto(f"{BASE_URL}/auth/login", wait_until="domcontentloaded")
        self.page.wait_for_selector("[data-test='email']", state="visible", timeout=60_000)
        return self

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def open_register(self) -> "AuthPage":
        self.page.goto(f"{BASE_URL}/auth/register", wait_until="domcontentloaded")
        self.page.wait_for_selector("[data-test='first-name']", state="visible", timeout=60_000)
        return self

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        dob: str = "1990-01-01",
        country: str = "US",
        postal_code: str = "12345",
        house_number: str = "1",
        street: str = "Main St",
        city: str = "Testville",
        state: str = "TX",
        phone: str = "5551234567",
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.dob_input.fill(dob)
        self.country_select.select_option(country)
        self.postal_code_input.fill(postal_code)
        self.house_number_input.fill(house_number)
        self.street_input.fill(street)
        self.city_input.fill(city)
        self.state_input.fill(state)
        self.phone_input.fill(phone)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.register_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()
