# UI Selectors — Practice Software Testing

> Status: Verified against live Angular source (testsmith-io/practice-software-testing sprint5).
> Tool: Playwright Python (`page.locator(...)`)

Base URL: https://practicesoftwaretesting.com

---

## Navigation / Header

| Element            | Selector                                      |
|--------------------|-----------------------------------------------|
| Home / Logo        | `a[href="/"]` or `[data-test="nav-logo"]`     |
| Search bar         | `[data-test="search-query"]`                  |
| Search button      | `[data-test="search-submit"]`                 |
| Cart icon          | `[data-test="nav-cart"]`                      |
| Sign In link       | `[data-test="nav-sign-in"]`                   |
| User menu (dropdown toggle) | `[data-test="nav-menu"]`             |
| Admin link         | `[data-test="nav-admin"]`                     |
| Categories filter  | `[data-test="category-link"]` (multiple)      |

---

## Product Listing (Homepage / Search Results)

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Product card         | `[data-test="product"]`                       |
| Product name         | `[data-test="product-name"]`                  |
| Product price        | `[data-test="product-price"]`                 |
| Product card link    | `[data-test="product"] a`                     |
| Sort dropdown        | `[data-test="sort"]`                          |
| Category sidebar     | `[data-test="category"]`                      |

---

## Product Detail Page

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Product name         | `[data-test="product-name"]`                  |
| Product price        | `[data-test="product-price"]`                 |
| Product description  | `[data-test="product-description"]`           |
| Quantity input       | `[data-test="quantity"]`                      |
| Add to Cart button   | `[data-test="add-to-cart"]`                   |
| Add to Favourites    | `[data-test="add-to-favorites"]`              |
| Related products     | `[data-test="related-product"]`               |

---

## Cart

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Cart item row        | `[data-test="cart-item"]`                     |
| Item quantity input  | `[data-test="cart-quantity"]`                 |
| Remove item button   | `[data-test="cart-remove"]`                   |
| Cart total           | `[data-test="cart-total"]`                    |
| Proceed to checkout  | `[data-test="proceed-1"]`                     |

---

## Auth Pages

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Email input          | `[data-test="email"]`                         |
| Password input       | `[data-test="password"]`                      |
| Login submit         | `[data-test="login-submit"]`                  |
| Register link        | `[data-test="register-link"]`                 |
| First name           | `[data-test="first-name"]`                    |
| Last name            | `[data-test="last-name"]`                     |
| Register submit      | `[data-test="register-submit"]`               |
| Forgot password link | `[data-test="forgot-password"]`               |
| TOTP input           | `[data-test="totp-input"]`                    |

---

## Checkout — Address Step

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| First name           | `[data-test="first-name"]`                    |
| Last name            | `[data-test="last-name"]`                     |
| Address line         | `[data-test="address"]`                       |
| City                 | `[data-test="city"]`                          |
| State                | `[data-test="state"]`                         |
| Country dropdown     | `[data-test="country"]`                       |
| Postcode             | `[data-test="postcode"]`                      |
| Proceed button       | `[data-test="proceed-2"]`                     |

---

## Checkout — Payment Step

| Element                   | Selector                                         |
|---------------------------|--------------------------------------------------|
| Payment method dropdown   | `[data-test="payment-method"]`                   |
| Bank name                 | `[data-test="bank-name"]`                        |
| Account name              | `[data-test="account-name"]`                     |
| Account number            | `[data-test="account-number"]`                   |
| Gift card number          | `[data-test="gift-card-number"]`                 |
| Validation code           | `[data-test="validation-code"]`                  |
| Credit card number        | `[data-test="credit-card-number"]`               |
| Expiration date           | `[data-test="expiration-date"]`                  |
| CVV                       | `[data-test="cvv"]`                              |
| Card holder name          | `[data-test="card-holder-name"]`                 |
| Monthly installments      | `[data-test="monthly-installments"]`             |
| Finish button             | `[data-test="finish"]`                           |
| Payment confirmation msg  | `[data-test="payment-success-message"]`          |

---

## Account Pages (`/account`)

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Orders tab           | `[data-test="nav-orders"]`                    |
| Favourites tab       | `[data-test="nav-favorites"]`                 |
| Profile tab          | `[data-test="nav-profile"]`                   |
| Invoice row          | `[data-test="invoice-row"]`                   |
| Download PDF button  | `[data-test="download-pdf"]`                  |

---

## Contact Page (`/contact`)

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Name input           | `[data-test="name"]`                          |
| Email input          | `[data-test="email"]`                         |
| Subject input        | `[data-test="subject"]`                       |
| Message textarea     | `[data-test="message"]`                       |
| Submit button        | `[data-test="contact-submit"]`                |
| Success message      | `[data-test="contact-success"]`               |

---

## Admin Pages (`/admin`)

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Products nav         | `[data-test="admin-products"]`                |
| Categories nav       | `[data-test="admin-categories"]`              |
| Brands nav           | `[data-test="admin-brands"]`                  |
| Users nav            | `[data-test="admin-users"]`                   |
| Invoices nav         | `[data-test="admin-invoices"]`                |
| Reports nav          | `[data-test="admin-reports"]`                 |
| Add new button       | `[data-test="add-new"]`                       |
| Save/Submit button   | `[data-test="save"]`                          |
| Delete button        | `[data-test="delete"]`                        |

---

## Toasts / Alerts

| Element              | Selector                                      |
|----------------------|-----------------------------------------------|
| Success toast        | `[data-test="toast-success"]`                 |
| Error toast          | `[data-test="toast-error"]`                   |
| Form error message   | `.invalid-feedback`, `[data-test="error-msg"]`|

---

> Note: `data-test` attributes are commonly used in this app. Verify each selector
> against the live DOM before writing tests. Use browser DevTools or Playwright's
> `page.pause()` to inspect elements.
