# API Reference — Practice Software Testing

Base URL: `https://api.practicesoftwaretesting.com`
Auth: `Authorization: Bearer <token>` (JWT, ~120s TTL)

---

## Authentication

| Method | Path                    | Auth | Body / Params                                  | Response                              |
|--------|-------------------------|------|------------------------------------------------|---------------------------------------|
| POST   | /users/login            | No   | `{email, password, totp?}`                     | `{access_token, token_type, expires_in}` or `{requires_totp: true}` |
| POST   | /users/register         | No   | `{first_name, last_name, email, password, ...}`| user object                           |
| GET    | /users/logout           | Yes  | —                                              | 200                                   |
| GET    | /users/refresh          | Yes  | —                                              | new `{access_token, ...}`             |
| POST   | /users/forgot-password  | No   | `{email}`                                      | 200                                   |
| POST   | /users/change-password  | Yes  | `{current_password, new_password}`             | 200                                   |

---

## Users (Admin)

| Method | Path            | Auth  | Notes                  |
|--------|-----------------|-------|------------------------|
| GET    | /users          | Admin | List all users         |
| GET    | /users/search   | Admin | Search users           |
| GET    | /users/me       | Yes   | Current user profile   |
| GET    | /users/{id}     | Admin | Get user by ID         |
| PUT    | /users/{id}     | Admin | Update user            |
| PATCH  | /users/{id}     | Admin | Partial update         |
| DELETE | /users/{id}     | Admin | Delete user            |

---

## Products

| Method | Path                        | Auth  | Notes               |
|--------|-----------------------------|-------|---------------------|
| GET    | /products                   | No    | List (cached)       |
| GET    | /products/search            | No    | Search by keyword   |
| GET    | /products/{id}              | No    | Single product      |
| GET    | /products/{id}/related      | No    | Related products    |
| POST   | /products                   | Admin | Create product      |
| PUT    | /products/{id}              | Admin | Update product      |
| PATCH  | /products/{id}              | Admin | Partial update      |
| DELETE | /products/{id}              | Admin | Delete product      |
| GET    | /products/{id}/specs        | No    | Product specs       |
| GET    | /products/{id}/specs/{sid}  | No    | Single spec         |
| POST   | /products/{id}/specs        | Admin | Add spec            |
| PUT    | /products/{id}/specs/{sid}  | Admin | Update spec         |
| DELETE | /products/{id}/specs/{sid}  | Admin | Delete spec         |
| GET    | /product-specs/names        | No    | All spec name keys  |

---

## Categories

| Method | Path                 | Auth  | Notes           |
|--------|----------------------|-------|-----------------|
| GET    | /categories          | No    | List (cached)   |
| GET    | /categories/tree     | No    | Nested tree     |
| GET    | /categories/search   | No    | Search          |
| POST   | /categories          | Admin | Create          |
| PUT    | /categories/{id}     | Admin | Update          |
| PATCH  | /categories/{id}     | Admin | Partial update  |
| DELETE | /categories/{id}     | Admin | Delete          |

---

## Brands

| Method | Path              | Auth  | Notes    |
|--------|-------------------|-------|----------|
| GET    | /brands           | No    | List     |
| GET    | /brands/search    | No    | Search   |
| GET    | /brands/{id}      | No    | Single   |
| POST   | /brands           | Admin | Create   |
| PUT    | /brands/{id}      | Admin | Update   |
| PATCH  | /brands/{id}      | Admin | Partial  |
| DELETE | /brands/{id}      | Admin | Delete   |

---

## Cart

| Method | Path                                  | Auth | Notes                   |
|--------|---------------------------------------|------|-------------------------|
| POST   | /carts                                | No   | Create cart → cart ID   |
| POST   | /carts/{id}                           | No   | Add item `{product_id, quantity}` |
| GET    | /carts/{id}                           | No   | Get cart contents       |
| PUT    | /carts/{id}/product/quantity          | No   | Update quantity         |
| DELETE | /carts/{cartId}/product/{productId}   | No   | Remove item             |
| DELETE | /carts/{cartId}                       | No   | Delete cart             |

---

## Invoices / Orders

| Method | Path                              | Auth  | Notes                    |
|--------|-----------------------------------|-------|--------------------------|
| GET    | /invoices                         | Yes   | List own invoices        |
| GET    | /invoices/search                  | Admin | Search all invoices      |
| GET    | /invoices/{id}                    | Yes   | Get invoice              |
| GET    | /invoices/{id}/download-pdf       | Yes   | Download PDF             |
| GET    | /invoices/{id}/download-pdf-status| Yes   | PDF generation status    |
| POST   | /invoices                         | Yes   | Create order             |
| POST   | /invoices/guest                   | No    | Guest checkout           |
| PUT    | /invoices/{id}                    | Admin | Update invoice           |
| PUT    | /invoices/{id}/status             | Admin | Update order status      |
| PATCH  | /invoices/{id}                    | Admin | Partial update           |

---

## Favourites

| Method | Path              | Auth | Notes         |
|--------|-------------------|------|---------------|
| GET    | /favorites        | Yes  | List          |
| POST   | /favorites        | Yes  | Add `{product_id}` |
| GET    | /favorites/{id}   | Yes  | Single        |
| DELETE | /favorites/{id}   | Yes  | Remove        |

---

## Messages / Contact

| Method | Path                          | Auth  | Notes               |
|--------|-------------------------------|-------|---------------------|
| GET    | /messages                     | Admin | List messages       |
| POST   | /messages                     | No    | Send message        |
| GET    | /messages/{id}                | Admin | Get message         |
| POST   | /messages/{id}/reply          | Admin | Reply               |
| POST   | /messages/{id}/attach-file    | Admin | Attach file         |
| PUT    | /messages/{id}/status         | Admin | Update status       |

---

## Payments

| Method | Path            | Auth | Notes                         |
|--------|-----------------|------|-------------------------------|
| POST   | /payment/check  | Yes  | Validate & process payment    |

---

## Reports (Admin, rate-limited)

| Method | Path                                      |
|--------|-------------------------------------------|
| GET    | /reports/total-sales-of-years             |
| GET    | /reports/total-sales-per-country          |
| GET    | /reports/top10-purchased-products         |
| GET    | /reports/top10-best-selling-categories    |
| GET    | /reports/customers-by-country             |
| GET    | /reports/average-sales-per-month          |
| GET    | /reports/average-sales-per-week           |

---

## 2FA / TOTP

| Method | Path               | Auth | Notes              |
|--------|--------------------|------|--------------------|
| POST   | /totp/setup        | Yes  | Enable 2FA         |
| POST   | /totp/verify       | No   | Verify TOTP code   |
| POST   | /totp/login/totp   | No   | Login with TOTP    |

---

## Misc

| Method | Path                  | Auth | Notes               |
|--------|-----------------------|------|---------------------|
| GET    | /status               | No   | App version + env   |
| GET    | /images               | No   | List images         |
| GET    | /postcode-lookup      | No   | Validate postcode   |
| POST   | /refresh              | No   | DB migration flush  |
| GET    | /auth/social-login    | No   | Get OAuth URL       |
| GET    | /auth/cb/google       | No   | Google OAuth CB     |
| GET    | /auth/cb/github       | No   | GitHub OAuth CB     |
