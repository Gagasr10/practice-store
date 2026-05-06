# Business Rules — Practice Software Testing

Base URL: https://practicesoftwaretesting.com
API URL:  https://api.practicesoftwaretesting.com

---

## Users & Roles

| Role  | Email                                    | Password   |
|-------|------------------------------------------|------------|
| admin | admin@practicesoftwaretesting.com        | welcome01  |
| user  | customer@practicesoftwaretesting.com     | welcome01  |
| user  | customer2@practicesoftwaretesting.com    | welcome01  |
| user  | customer3@practicesoftwaretesting.com    | pass123    |

- Unauthenticated users can browse products and search.
- Only authenticated users can add to favourites, place orders, view invoice history.
- Only admin users can create/update/delete products, categories, brands, manage users, view reports.
- Accounts can be locked after failed login attempts (HTTP 423).
- Disabled accounts receive HTTP 403 on login.
- Two-factor authentication (TOTP) is supported; when enabled, login returns `requires_totp: true` and an intermediate access_token.

---

## Authentication

- Method: JWT Bearer token
- Login endpoint: `POST /users/login`
- Token expires in: ~120 seconds (short; refresh via `GET /users/refresh`)
- Token is passed in: `Authorization: Bearer <token>` header
- Social login: Google and GitHub (OAuth callbacks)

---

## Product Catalogue

### Categories (tree)

| Parent      | Subcategories                                      |
|-------------|----------------------------------------------------|
| Hand Tools  | Hammer, Hand Saw, Wrench, Screwdriver, Pliers, Chisels, Measures |
| Power Tools | Grinder, Sander, Saw, Drill                        |
| Other       | Tool Belts, Storage Solutions, Workbench, Safety Gear, Fasteners |

- Products belong to exactly one subcategory.
- Products have: name, description, price, stock, brand, images, related products.
- Products can be searched by name/description via `GET /products/search`.
- Related products are returned via `GET /products/{id}/related`.
- Product specs (additional attributes) are managed via `/products/{id}/specs`.

---

## Cart

- A cart is created independently (not tied to a user session initially).
- `POST /carts` → creates a cart, returns cart ID.
- `POST /carts/{id}` → adds a product + quantity to the cart.
- `PUT /carts/{id}/product/quantity` → updates item quantity.
- `DELETE /carts/{cartId}/product/{productId}` → removes one item.
- `DELETE /carts/{cartId}` → deletes the entire cart.
- No stock reservation during cart phase (stock checked at checkout).

---

## Checkout Flow (4 Steps)

1. **Cart** — Review items, quantities, subtotal.
2. **Login** — Must be authenticated to proceed (redirects to login if not).
3. **Address** — Shipping/billing address (must be valid to advance).
4. **Payment** — Choose payment method and submit.

Address validation blocks step progression until the form is valid.

---

## Payment Methods

| Method              | Required Fields                                            | Validation                                                   |
|---------------------|------------------------------------------------------------|--------------------------------------------------------------|
| Bank Transfer       | bank_name, account_name, account_number                    | bank_name: letters+spaces; account_number: digits only       |
| Gift Card           | gift_card_number, validation_code                          | alphanumeric only                                            |
| Credit Card         | credit_card_number, expiration_date, cvv, card_holder_name | card: XXXX-XXXX-XXXX-XXXX; expiry: MM/YYYY (future); CVV: 3-4 digits |
| Buy Now Pay Later   | monthly_installments                                       | required                                                     |
| Cash on Delivery    | (none)                                                     | no extra fields                                              |

---

## Invoices / Orders

- Created via `POST /invoices` (authenticated) or `POST /invoices/guest`.
- Can be viewed, searched, and downloaded as PDF.
- Invoice status can be updated by admin (`PUT /invoices/{id}/status`).

---

## Favourites (Wishlist)

- Authenticated users can add/remove products from favourites.
- `GET /favorites`, `POST /favorites`, `DELETE /favorites/{id}`.

---

## Contact / Messages

- Users can send messages via `POST /messages`.
- Admin can reply (`POST /messages/{id}/reply`) and attach files.
- Message status is updatable by admin.

---

## Reports (Admin only, rate-limited)

- Total sales per year / per country
- Top 10 purchased products
- Top 10 best-selling categories
- Customers by country
- Average sales per month / per week

---

## Postcode Lookup

- `GET /postcode-lookup` — validates/looks up a postcode (used in address step).
