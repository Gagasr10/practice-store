
# Project State

> This file is the memory between sessions.
> Every new session starts with: read this file first.
> Update this file at the end of every phase or significant session.

---

## Project info

| Field | Value |
|-------|-------|
| Project name | Practice Software Testing — E-commerce Store |
| Client | practicesoftwaretesting.com |
| Frontend URL | https://practicesoftwaretesting.com |
| API URL | https://api.practicesoftwaretesting.com |
| Swagger | https://api.practicesoftwaretesting.com/api/documentation |
| Testing tool | Playwright Python |
| CI tool | GitHub Actions |
| Started | 2026-04-30 |
| Last updated | 2026-05-02 |

---

## Phase status

| Phase | Status | Completed | Notes |
|-------|--------|-----------|-------|
| 1 — Understand | ✅ Done | 2026-04-30 | API routes, UI structure, auth, categories, flows |
| 2 — Domain | ✅ Done | 2026-04-30 | business-rules, api-reference, user-flows, ui-selectors, SKILL.md |
| 3 — Plan | ✅ Done | 2026-04-30 | test-plan.md: 76 tests, P0/P1/P2, folder structure, parallel strategy |
| 4 — Framework | ✅ Done | 2026-04-30 | Playwright Python scaffold: conftest, api/, pages/, smoke tests, regression/edge stubs |
| 5 — Tests | ✅ Done | 2026-05-01 | 67 tests implemented (regression + edge) |
| 5b — Live fix | ✅ Done | 2026-05-02 | All regression tests pass: 49 passed, 5 skipped, 1 xfailed, 0 failures |
| 6 — CI/CD | ✅ Done | 2026-05-02 | 3 workflows: smoke (push/PR), regression (nightly+PR), Allure Pages |
| 7 — Delivery | ⬜ Not started | — | — |

Status legend: ⬜ Not started · 🔄 In progress · ✅ Done

---

## Current state

### Where we left off
Phase 6 done — 3 GitHub Actions workflows created:
- `.github/workflows/smoke.yml` — P0 smoke tests on every push/PR, ≤15 min, no retries, JUnit artifact
- `.github/workflows/regression.yml` — P1 regression nightly (02:00 UTC) + PR to main + manual dispatch, ≤30 min, with --reruns 2, JUnit + Allure artifacts
- `.github/workflows/allure-report.yml` — publishes Allure HTML with history to GitHub Pages (gh-pages branch /allure) after each regression run

### Next step
Phase 7 — Delivery: finalize README, repo setup instructions, and hand-off documentation.

### Blockers
None

---

## Key decisions

| Decision | Value | Reason |
|----------|-------|--------|
| Testing tool | Playwright Python | User choice |
| CI tool | GitHub Actions | User choice |
| Browser | Chromium (default) | Playwright default |
| Base URL | https://practicesoftwaretesting.com | User confirmed |
| API Base URL | https://api.practicesoftwaretesting.com | User confirmed |
| Auth mechanism | JWT Bearer (~120s TTL) + refresh | Laravel API design |
| Parallel execution | pytest-xdist, 4 workers (CI) | Independent tests, GHA runner cores |

---

## Test accounts

| Role  | Email                                     | Password  | Notes |
|-------|-------------------------------------------|-----------|-------|
| admin | admin@practicesoftwaretesting.com         | welcome01 | Full admin access |
| user  | customer@practicesoftwaretesting.com      | welcome01 | Primary test user |
| user  | customer2@practicesoftwaretesting.com     | welcome01 | Secondary test user |
| user  | customer3@practicesoftwaretesting.com     | pass123   | Alt password user |

---

## Test suite progress

| Suite | Written | Passing | Notes |
|-------|---------|---------|-------|
| Smoke (P0) | 10 | ? | Not run as standalone smoke yet |
| Regression (P1) | 54 | 49 pass / 5 skip / 1 xfail | All pass against live app as of 2026-05-02 |
| Edge cases (P2) | 12 | ? | Not run standalone; xfail on locked/disabled account |

---

## Known issues

| Issue | Type | Status |
|-------|------|--------|
| test_checkout_buy_now_pay_later / cash_on_delivery flaky in full run | flaky | Mitigated with --reruns 2; root cause: shared backend cart state between tests |
| test_unauthenticated_user_redirected needs rerun sometimes | flaky | Mitigated with --reruns 2 |
| Admin product edit form: Angular doesn't pre-populate brand/category/stock on edit page | app-bug | Workaround in test: fill all required fields explicitly |
| Invoice status: COMPLETED→PENDING returns 404 (only ON_HOLD/AWAITING_FULFILLMENT/SHIPPED valid from COMPLETED) | app-bug | Workaround in test |

Type: test-bug / app-bug / flaky / blocked

---

## Domain files status

| File | Status | Notes |
|------|--------|-------|
| SKILL.md | ✅ Done | Domain summary + quick-ref |
| business-rules.md | ✅ Done | Roles, auth, cart, checkout, payments, categories |
| api-reference.md | ✅ Done | All endpoints with method, auth, notes |
| ui-selectors.md | ✅ Done | data-test selectors — needs live verification |
| user-flows.md | ✅ Done | 12 end-to-end user flows |

---

## CI/CD status

| Component | Status | URL |
|-----------|--------|-----|
| Smoke pipeline | ✅ `.github/workflows/smoke.yml` | Triggers on every push/PR |
| Regression pipeline | ✅ `.github/workflows/regression.yml` | Nightly 02:00 UTC + PR to main |
| Allure Pages | ✅ `.github/workflows/allure-report.yml` | Published to gh-pages /allure after regression |

---

## Session log

| Date | What was done |
|------|--------------|
| 2026-04-30 | Project initialized — stack: Playwright Python + GitHub Actions |
| 2026-04-30 | Phase 1 done — app explored: API routes, auth, categories, UI structure |
| 2026-04-30 | Phase 2 done — domain files written: SKILL.md, business-rules, api-reference, ui-selectors, user-flows |
| 2026-04-30 | Phase 3 done — test-plan.md: 76 tests (P0/P1/P2), folder layout, pytest-xdist parallel strategy |
| 2026-04-30 | Phase 4 done — Playwright Python framework scaffolded: api/, pages/, conftest, smoke tests (10), regression/edge stubs (66) |
| 2026-05-01 | Phase 5 done — 67 regression+edge tests implemented (test_auth, products, cart, checkout, account, contact, admin, guest, 2fa, cart_edge, misc) |
| 2026-05-02 | Phase 5b done — ran all regression tests against live app, fixed all selector/assertion mismatches: 49 passed, 5 skipped, 1 xfailed, 0 failures |
| 2026-05-02 | Phase 6 done — GitHub Actions CI/CD: smoke.yml, regression.yml, allure-report.yml; pytest-rerunfailures added to requirements.txt |
