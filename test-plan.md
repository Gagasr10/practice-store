# Test Plan — Practice Software Testing

---

## Scope

| In scope | Out of scope |
|----------|--------------|
| UI flows (Playwright) | Mobile app (Android/iOS) |
| API flows (requests via pytest) | GraphQL endpoints |
| Auth, cart, checkout, account, admin, contact | Social login (OAuth — external provider) |
| All 5 payment methods | Email delivery (forgot password) |
| Admin CRUD + reports | PDF content validation |

---

## Test Priorities

### P0 — Smoke (run on every push, must be green to deploy)

| ID   | Area     | Test case                                      | Type |
|------|----------|------------------------------------------------|------|
| S01  | Health   | Homepage loads, product grid visible           | UI   |
| S02  | Auth     | Login with valid credentials (customer)        | UI   |
| S03  | Auth     | Login returns Bearer token                     | API  |
| S04  | Products | Product listing returns results                | API  |
| S05  | Products | Product detail page loads                      | UI   |
| S06  | Search   | Search by keyword returns matching products    | UI   |
| S07  | Cart     | Add product to cart                            | UI   |
| S08  | Checkout | Full checkout — Cash on Delivery (happy path)  | UI   |
| S09  | Auth     | Logout clears session                          | UI   |
| S10  | Admin    | Admin can log in and reach dashboard           | UI   |

**Target: ≤ 3 min total, headless Chromium.**

---

### P1 — Regression (run nightly + on PR to main)

#### Authentication
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R01  | Login with wrong password → error shown             | UI   |
| R02  | Login with unknown email → error shown              | UI   |
| R03  | Login locked account → 423 response                 | API  |
| R04  | Login disabled account → 403 response               | API  |
| R05  | Register new user → can log in afterwards           | UI   |
| R06  | Register duplicate email → validation error         | UI   |
| R07  | Register mismatched passwords → validation error    | UI   |
| R08  | Change password (authenticated)                     | UI   |
| R09  | Refresh token returns new access token              | API  |
| R10  | Forgot password endpoint accepts valid email        | API  |

#### Products & Search
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R11  | Filter products by category                         | UI   |
| R12  | Filter products by brand                            | UI   |
| R13  | Sort products by price ascending / descending       | UI   |
| R14  | Search returns empty state for unknown keyword      | UI   |
| R15  | Product detail shows name, price, description       | UI   |
| R16  | Related products section visible on product page    | UI   |
| R17  | Product specs displayed correctly                   | UI   |
| R18  | GET /products pagination (page + per_page params)   | API  |
| R19  | GET /products/search filters by query               | API  |
| R20  | GET /categories/tree returns nested structure       | API  |

#### Cart
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R21  | Add multiple products to cart                       | UI   |
| R22  | Update item quantity in cart                        | UI   |
| R23  | Remove single item from cart                        | UI   |
| R24  | Cart persists across page navigation                | UI   |
| R25  | POST /carts then POST /carts/{id} (API cart flow)   | API  |
| R26  | DELETE /carts/{id}/product/{pid} removes item       | API  |

#### Checkout — Payment Methods
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R27  | Checkout — Bank Transfer (valid fields)             | UI   |
| R28  | Checkout — Gift Card (valid fields)                 | UI   |
| R29  | Checkout — Credit Card (valid fields)               | UI   |
| R30  | Checkout — Buy Now Pay Later                        | UI   |
| R31  | Checkout — Cash on Delivery                         | UI   |
| R32  | Credit card — invalid format rejected               | UI   |
| R33  | Credit card — past expiry date rejected             | UI   |
| R34  | Address step — blank fields block progression       | UI   |
| R35  | Address step — postcode lookup populates fields     | UI   |
| R36  | Unauthenticated user redirected to login at step 2  | UI   |

#### Account & Orders
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R37  | Authenticated user sees order history               | UI   |
| R38  | Invoice detail shows correct items and total        | UI   |
| R39  | Download PDF endpoint returns file                  | API  |
| R40  | Add product to favourites                           | UI   |
| R41  | Remove product from favourites                      | UI   |
| R42  | GET /favorites returns user's favourites            | API  |

#### Contact
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R43  | Contact form submits successfully                   | UI   |
| R44  | Contact form — empty required fields blocked        | UI   |
| R45  | POST /messages creates message record               | API  |

#### Admin
| ID   | Test case                                           | Type |
|------|-----------------------------------------------------|------|
| R46  | Admin creates new product                           | UI   |
| R47  | Admin edits existing product                        | UI   |
| R48  | Admin deletes product                               | UI   |
| R49  | Admin creates category                              | API  |
| R50  | Admin creates brand                                 | API  |
| R51  | Admin updates invoice status                        | API  |
| R52  | Admin views user list                               | UI   |
| R53  | GET /reports/top10-purchased-products (admin token) | API  |
| R54  | Non-admin token rejected on admin endpoints → 403   | API  |

---

### P2 — Edge Cases (run on-demand / weekly)

| ID   | Test case                                            | Type |
|------|------------------------------------------------------|------|
| E01  | Guest checkout via POST /invoices/guest              | API  |
| E02  | TOTP setup and login with 2FA code                   | API  |
| E03  | Cart — add 0 or negative quantity → rejected         | API  |
| E04  | Cart — add out-of-stock product → error              | API  |
| E05  | Reports endpoint rate-limited after N requests       | API  |
| E06  | Postcode lookup with invalid postcode                | API  |
| E07  | Long product name / XSS payload in search field      | UI   |
| E08  | Concurrent adds to same cart (race condition check)  | API  |
| E09  | Token expired — refresh and retry                    | API  |
| E10  | Admin cannot be deleted via DELETE /users/{id}       | API  |
| E11  | Category tree depth — no orphan categories           | API  |
| E12  | Invoice PDF status endpoint polling                  | API  |

---

## Folder Structure

```
practice-store/
├── tests/
│   ├── smoke/
│   │   ├── test_health.py          # S01
│   │   ├── test_auth_smoke.py      # S02, S03, S09
│   │   ├── test_products_smoke.py  # S04, S05, S06
│   │   ├── test_cart_smoke.py      # S07
│   │   └── test_checkout_smoke.py  # S08
│   ├── regression/
│   │   ├── test_auth.py            # R01-R10
│   │   ├── test_products.py        # R11-R20
│   │   ├── test_cart.py            # R21-R26
│   │   ├── test_checkout.py        # R27-R36
│   │   ├── test_account.py         # R37-R42
│   │   ├── test_contact.py         # R43-R45
│   │   └── test_admin.py           # R46-R54
│   └── edge/
│       ├── test_guest.py           # E01
│       ├── test_2fa.py             # E02
│       ├── test_cart_edge.py       # E03-E04, E08
│       └── test_misc.py            # E05-E07, E09-E12
├── pages/                          # Page Object Model
│   ├── base_page.py
│   ├── home_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── auth_page.py
│   ├── account_page.py
│   ├── contact_page.py
│   └── admin/
│       ├── dashboard_page.py
│       ├── products_page.py
│       └── invoices_page.py
├── api/                            # Raw API helpers (requests)
│   ├── client.py                   # Base client with auth header
│   ├── auth.py                     # login(), logout(), refresh()
│   ├── products.py
│   ├── cart.py
│   ├── invoices.py
│   └── users.py
├── fixtures/
│   └── conftest.py                 # shared pytest fixtures
├── data/
│   └── test_data.py                # constants: URLs, accounts, payloads
├── conftest.py                     # root conftest: browser, base_url
├── pytest.ini
└── requirements.txt
```

---

## Patterns & Conventions

### State setup: API-first
- Use the REST API (not the UI) to set up preconditions (login, create cart, seed product).
- UI tests start from the correct state, not from the homepage every time.
- Teardown via API where possible (delete cart, remove favourite, delete test product).

### Page Object Model
- One class per page, in `pages/`.
- Methods return `self` for chaining or the extracted value — never raw locators.
- Locators defined once per page class, not inline in tests.

### Auth fixture
- `@pytest.fixture` `user_token` → calls `POST /users/login`, returns token string.
- `@pytest.fixture` `admin_token` → same for admin credentials.
- Playwright `browser_context` fixture injects token into `localStorage` or `Authorization` header via `APIRequestContext`.

### Test isolation
- Each test creates its own cart ID.
- No shared mutable state between tests.
- Tests in `smoke/` and `regression/` can run in any order.

---

## Parallel Execution

| Setting | Value | Reason |
|---------|-------|--------|
| Runner | `pytest-xdist` | Native pytest parallelism |
| Workers | `auto` (CI: 4) | Match GHA runner cores |
| Scope | per-test | Tests are independent |
| Browser | Chromium headless | Fastest; consistent in CI |
| Headed mode | local only via `--headed` flag | Debugging only |

Command: `pytest tests/ -n auto --browser chromium`

---

## CI Pipelines (Phase 6 detail)

| Pipeline | Trigger | Suite | Target time |
|----------|---------|-------|-------------|
| Smoke | push to any branch | `tests/smoke/` | < 3 min |
| Regression | nightly + PR to main | `tests/regression/` | < 15 min |
| Edge | manual / weekly | `tests/edge/` | < 10 min |
| Report | after regression | Allure report publish | — |

---

## Total Test Count

| Priority | Count | Type breakdown |
|----------|-------|----------------|
| P0 Smoke | 10 | 7 UI · 3 API |
| P1 Regression | 54 | 38 UI · 16 API |
| P2 Edge | 12 | 4 UI · 8 API |
| **Total** | **76** | **49 UI · 27 API** |
