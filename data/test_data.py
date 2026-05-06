BASE_URL = "https://practicesoftwaretesting.com"
API_BASE_URL = "https://api.practicesoftwaretesting.com"

# Test accounts (seeded by the app)
ADMIN_EMAIL = "admin@practicesoftwaretesting.com"
ADMIN_PASSWORD = "welcome01"

# customer2@ is used as the primary test user because customer@ is frequently
# corrupted by other shared-environment users changing its password.
USER_EMAIL = "customer2@practicesoftwaretesting.com"
USER_PASSWORD = "welcome01"

# Use customer3 for wrong-password tests to avoid locking USER_EMAIL
USER3_EMAIL = "customer3@practicesoftwaretesting.com"
USER3_PASSWORD = "pass123"

# localStorage key used by the Angular app to store the JWT
AUTH_TOKEN_KEY = "auth-token"

# Checkout — address payload used in tests
DEFAULT_ADDRESS = {
    "street": "Main Street",
    "house_number": "123",
    "city": "Testville",
    "state": "Test State",
    "country": "US",
    "postal_code": "12345",
}

# Payment payloads
PAYMENT_BANK_TRANSFER = {
    "method": "Bank Transfer",
    "bank_name": "Test Bank",
    "account_name": "Test User",
    "account_number": "1234567890",
}

PAYMENT_GIFT_CARD = {
    "method": "Gift Card",
    "gift_card_number": "GC123456",
    "validation_code": "VAL123",
}

PAYMENT_CREDIT_CARD = {
    "method": "Credit Card",
    "credit_card_number": "1234-5678-9012-3456",
    "expiration_date": "12/2028",
    "cvv": "123",
    "card_holder_name": "Test User",
}

PAYMENT_BNPL = {
    "method": "Buy Now Pay Later",
    "monthly_installments": "3",
}

PAYMENT_COD = {
    "method": "Cash on Delivery",
}
