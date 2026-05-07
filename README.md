# Practice Store — Playwright Test Suite

End-to-end + API test automation for [practicesoftwaretesting.com](https://practicesoftwaretesting.com).

**Stack:** Python · Playwright · pytest · GitHub Actions · Allure

---

## Quick start

```bash
# 1. Clone
git clone <repo-url>
cd practice-store

# 2. Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browser
playwright install chromium --with-deps

# 5. Run smoke tests (≈ 2 min)
pytest tests/smoke/ -m smoke -v
```

---

## Running tests

| Command | What runs |
|---------|-----------|
| `pytest tests/smoke/ -m smoke -v` | P0 smoke (10 tests, ~2 min) |
| `pytest tests/regression/ -m regression -v` | P1 regression (55 tests, ~4 min) |
| `pytest tests/edge/ -m edge -v` | P2 edge cases (12 tests, ~4 min) |
| `pytest -v` | Everything |
| `pytest tests/regression/ -m regression -v -n 4` | Regression in parallel (4 workers) |

### Allure report (local)

```bash
pytest tests/regression/ -m regression --alluredir=allure-results
allure serve allure-results
```

> Requires [Allure CLI](https://allurereport.org/docs/install/) installed separately.

---

## Project structure

```
practice-store/
├── api/                    # API client wrappers (requests)
│   ├── client.py           # Base HTTP client
│   ├── auth.py             # Login / token management
│   ├── products.py         # Products endpoints
│   ├── cart.py             # Cart endpoints
│   └── invoices.py         # Invoice / order endpoints
│
├── pages/                  # Playwright page objects
│   ├── base_page.py
│   ├── auth_page.py
│   ├── home_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── account_page.py
│   ├── contact_page.py
│   └── admin/
│       ├── dashboard_page.py
│       └── products_page.py
│
├── tests/
│   ├── smoke/              # P0 — run on every push/PR
│   ├── regression/         # P1 — nightly + PR to main
│   └── edge/               # P2 — on demand / weekly
│
├── data/
│   └── test_data.py        # Shared constants and test fixtures
│
├── .github/workflows/
│   ├── smoke.yml           # Smoke CI (every push/PR)
│   ├── regression.yml      # Regression CI (nightly + PR to main)
│   └── allure-report.yml   # Publishes Allure HTML to GitHub Pages
│
├── conftest.py             # pytest fixtures (browser, pages, API clients)
├── pytest.ini              # Base URL, markers, default addopts
├── requirements.txt
│
├── test-plan.md            # Full test plan (76 tests, P0/P1/P2)
├── business-rules.md       # Domain rules: auth, cart, checkout, payments
├── api-reference.md        # All API endpoints
├── user-flows.md           # 12 end-to-end user flows
└── ui-selectors.md         # data-test attribute reference
```

---

## CI/CD

| Workflow | Trigger | Timeout | Report |
|----------|---------|---------|--------|
| **Smoke** | Every push, every PR | 15 min | JUnit artifact + PR check |
| **Regression** | Nightly 02:00 UTC, PR to `main`, manual | 30 min | JUnit + Allure artifact + PR check |
| **Allure Pages** | After each regression run | — | Published to `gh-pages` branch |

### Enable GitHub Pages

After the first regression run, enable Pages in **Settings → Pages**:
- Source: **Deploy from a branch**
- Branch: `gh-pages` / `/(root)`

The Allure report will be available at `https://<org>.github.io/<repo>/allure/`.

---

## Test accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@practicesoftwaretesting.com | welcome01 |
| Customer (primary) | customer@practicesoftwaretesting.com | welcome01 |
| Customer (secondary) | customer2@practicesoftwaretesting.com | welcome01 |
| Customer (alt password) | customer3@practicesoftwaretesting.com | pass123 |

Credentials are used only by tests against the shared demo environment — no secrets need to be stored in GitHub.

---

## Configuration

`pytest.ini` sets the base URL and default options:

```ini
[pytest]
base_url = https://practicesoftwaretesting.com
addopts  = -v --tb=short --reruns 2 --reruns-delay 2
```

To run against a different environment, override `base_url`:

```bash
pytest --base-url=https://staging.practicesoftwaretesting.com tests/smoke/ -m smoke
```

---

## Known issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| `test_unauthenticated_user_redirected` occasionally slow | P1 intermittent | `--reruns 2` in CI |
| Admin product edit — Angular doesn't pre-populate brand/category/stock | App bug | Tests fill all fields explicitly |
| Invoice status: `COMPLETED → PENDING` returns 404 | App bug | Tests use valid transitions only |

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| pip | latest |
| Node.js | Not required (Playwright installs Chromium via pip) |
| Allure CLI | Optional — only needed for local HTML reports |

---

## Markers

```
smoke       P0 — critical path, run on every push
regression  P1 — full feature regression, nightly
edge        P2 — edge cases, on demand
ui          Playwright browser tests
api         API-only tests (no browser)
```

Filter by marker: `pytest -m "regression and not edge" -v`
