# Domain Skill — Practice Software Testing

E-commerce tool shop for practicing test automation.
Stack: Angular frontend + Laravel REST API + JWT auth.

---

## App at a glance

| Item          | Value                                              |
|---------------|----------------------------------------------------|
| Frontend      | https://practicesoftwaretesting.com                |
| API           | https://api.practicesoftwaretesting.com            |
| Swagger       | https://api.practicesoftwaretesting.com/api/documentation |
| Auth          | JWT Bearer, ~120s TTL, refresh via GET /users/refresh |

---

## Key domain files

| File                  | What it contains                                      |
|-----------------------|-------------------------------------------------------|
| business-rules.md     | Users, roles, cart rules, checkout steps, payment methods, categories |
| api-reference.md      | Full endpoint table: method, path, auth requirement   |
| user-flows.md         | Step-by-step user journeys (12 flows)                 |
| ui-selectors.md       | Playwright locators for all major pages               |

---

## Test accounts

| Role  | Email                                     | Password  |
|-------|-------------------------------------------|-----------|
| admin | admin@practicesoftwaretesting.com         | welcome01 |
| user  | customer@practicesoftwaretesting.com      | welcome01 |
| user  | customer2@practicesoftwaretesting.com     | welcome01 |
| user  | customer3@practicesoftwaretesting.com     | pass123   |

---

## Critical business rules (quick ref)

- Guest can browse and add to cart; must log in to complete checkout.
- Checkout is a 4-step wizard: Cart → Login → Address → Payment.
- 5 payment methods: Bank Transfer, Gift Card, Credit Card, Buy Now Pay Later, Cash on Delivery.
- Token expires in ~120s — tests must refresh or re-login for long flows.
- Account lockout: HTTP 423. Disabled: HTTP 403.
- Categories: Hand Tools / Power Tools / Other (each with subcategories).
- Report endpoints are rate-limited.

---

## UI selector strategy

- Primary: `[data-test="..."]` attributes.
- Secondary: semantic HTML (labels, roles).
- Avoid: CSS class names (likely to change).
- Verify selectors in browser DevTools before writing tests.
