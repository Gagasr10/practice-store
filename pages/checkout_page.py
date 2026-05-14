from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Address step
        self.street = page.locator("[data-test='street']")
        self.house_number = page.locator("[data-test='house_number']")
        self.city = page.locator("[data-test='city']")
        self.state = page.locator("[data-test='state']")
        self.country = page.locator("[data-test='country']")
        self.postal_code = page.locator("[data-test='postal_code']")
        self.proceed_sign_in = page.locator("[data-test='proceed-2']")
        self.proceed_address = page.locator("[data-test='proceed-3']")

        # Payment step — selectors use underscores to match live data-test attributes
        self.payment_method = page.locator("[data-test='payment-method']")
        self.bank_name = page.locator("[data-test='bank_name']")
        self.account_name = page.locator("[data-test='account_name']")
        self.account_number = page.locator("[data-test='account_number']")
        self.gift_card_number = page.locator("[data-test='gift_card_number']")
        self.validation_code = page.locator("[data-test='validation_code']")
        self.credit_card_number = page.locator("[data-test='credit_card_number']")
        self.expiration_date = page.locator("[data-test='expiration_date']")
        self.cvv = page.locator("[data-test='cvv']")
        self.card_holder_name = page.locator("[data-test='card_holder_name']")
        self.monthly_installments = page.locator("[data-test='monthly_installments']")
        self.finish_button = page.locator("[data-test='finish']")
        self.payment_success = page.locator("[data-test='payment-success-message']")

    def proceed_from_sign_in(self) -> None:
        self.proceed_sign_in.click()

    def fill_address(self, address: dict) -> None:
        # country/postal_code/house_number are visible; the postcode API auto-populates
        # street/city/state (hidden inputs). force=True bypasses the visibility check.
        self.country.select_option(address["country"])
        self.postal_code.fill(address["postal_code"])
        self.house_number.fill(address["house_number"])
        self.street.fill(address["street"], force=True)
        self.city.fill(address["city"], force=True)
        self.state.fill(address["state"], force=True)

    def proceed_from_address(self) -> None:
        from playwright.sync_api import expect
        # The form triggers an async postcode lookup (postal_code + house_number →
        # API). While the lookup is pending the form is invalid and proceed-3 is
        # disabled even though all fields are filled. Wait for the loading indicator
        # to disappear before asserting the button is enabled.
        self.page.locator("[data-test='postcode-lookup-loading']").wait_for(
            state="hidden", timeout=20_000
        )
        expect(self.proceed_address).to_be_enabled(timeout=15_000)
        self.proceed_address.click()

    def select_payment_method(self, method: str) -> None:
        self.payment_method.select_option(method)

    def fill_bank_transfer(self, bank_name: str, account_name: str, account_number: str) -> None:
        self.bank_name.fill(bank_name)
        self.account_name.fill(account_name)
        self.account_number.fill(account_number)

    def fill_gift_card(self, card_number: str, validation_code: str) -> None:
        self.gift_card_number.fill(card_number)
        self.validation_code.fill(validation_code)

    def fill_credit_card(self, number: str, expiry: str, cvv: str, holder: str) -> None:
        self.credit_card_number.fill(number)
        self.expiration_date.fill(expiry)
        self.cvv.fill(cvv)
        self.card_holder_name.fill(holder)

    def fill_bnpl(self, installments: str) -> None:
        self.monthly_installments.select_option(installments)

    def finish(self) -> None:
        self.finish_button.click()

    def is_payment_confirmed(self) -> bool:
        return self.payment_success.is_visible()
